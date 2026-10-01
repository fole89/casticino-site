// Login GitHub per l'area di redazione delle news (admin/, Decap CMS).
// Cloudflare Worker: tiene la chiave segreta dell'applicazione OAuth di GitHub, che non può stare nel sito.
// Istruzioni per attivarlo: LEGGIMI.md nella stessa cartella.
//
// Variabili del Worker (Settings › Variables and Secrets):
//   GITHUB_CLIENT_ID      Client ID dell'applicazione OAuth di GitHub
//   GITHUB_CLIENT_SECRET  Client secret (come «Secret»)
//   ALLOWED_ORIGINS       indirizzi da cui si può accedere, separati da virgola
//                         es. https://fole89.github.io,https://casticino.ch,http://localhost:8000

const GITHUB = "https://github.com/login/oauth";

export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    // 1. l'area di redazione apre una finestra su /auth: si va al login di GitHub
    if (url.pathname === "/auth") {
      const state = crypto.randomUUID();
      const scope = url.searchParams.get("scope") || "public_repo";
      const go = new URL(`${GITHUB}/authorize`);
      go.searchParams.set("client_id", env.GITHUB_CLIENT_ID);
      go.searchParams.set("redirect_uri", `${url.origin}/callback`);
      go.searchParams.set("scope", scope);
      go.searchParams.set("state", state);
      return new Response(null, {
        status: 302,
        headers: {
          Location: go.toString(),
          "Set-Cookie": `cms_state=${state}; Path=/; HttpOnly; Secure; SameSite=Lax; Max-Age=600`,
        },
      });
    }

    // 2. GitHub torna su /callback con un codice: lo si scambia con il token e lo si passa all'area di redazione
    if (url.pathname === "/callback") {
      const cookie = request.headers.get("Cookie") || "";
      const atteso = (cookie.match(/(?:^|;\s*)cms_state=([^;]+)/) || [])[1];
      if (!atteso || atteso !== url.searchParams.get("state")) {
        return risposta(env, "error", { message: "Richiesta non valida: riprova ad accedere." });
      }
      const r = await fetch(`${GITHUB}/access_token`, {
        method: "POST",
        headers: { "Content-Type": "application/json", Accept: "application/json" },
        body: JSON.stringify({
          client_id: env.GITHUB_CLIENT_ID,
          client_secret: env.GITHUB_CLIENT_SECRET,
          code: url.searchParams.get("code"),
          redirect_uri: `${url.origin}/callback`,
        }),
      });
      const dati = await r.json();
      if (!dati.access_token) {
        return risposta(env, "error", { message: dati.error_description || "Accesso non riuscito." });
      }
      return risposta(env, "success", { token: dati.access_token, provider: "github" });
    }

    return new Response("Login dell'area di redazione CAS Ticino.", { status: 404 });
  },
};

// Pagina che passa il risultato alla finestra dell'area di redazione (protocollo di Decap CMS),
// solo se questa è su uno degli indirizzi ammessi.
function risposta(env, esito, contenuto) {
  const ammessi = (env.ALLOWED_ORIGINS || "").split(",").map((s) => s.trim()).filter(Boolean);
  const messaggio = `authorization:github:${esito}:${JSON.stringify(contenuto)}`;
  const html = `<!doctype html><meta charset="utf-8"><title>Accesso</title>
<p>Accesso in corso…</p>
<script>
(function () {
  var ammessi = ${JSON.stringify(ammessi)};
  function ricevi(e) {
    if (ammessi.indexOf(e.origin) === -1) return;
    window.removeEventListener("message", ricevi);
    window.opener.postMessage(${JSON.stringify(messaggio)}, e.origin);
    setTimeout(function () { window.close(); }, 500);
  }
  window.addEventListener("message", ricevi);
  window.opener && window.opener.postMessage("authorizing:github", "*");
})();
</script>`;
  return new Response(html, {
    headers: {
      "Content-Type": "text/html; charset=utf-8",
      "Set-Cookie": "cms_state=; Path=/; HttpOnly; Secure; SameSite=Lax; Max-Age=0",
      "Cache-Control": "no-store",
    },
  });
}
