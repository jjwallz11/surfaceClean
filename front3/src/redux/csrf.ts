import Cookies from "js-cookie";

interface CsrfFetchOptions extends RequestInit {
  headers?: HeadersInit & { "X-CSRF-Token"?: string };
}

export async function csrfFetch(url: string, options: CsrfFetchOptions = {}) {
  const opts: CsrfFetchOptions = {
    method: options.method || "GET",
    credentials: "include",
    ...options,
  };

  const headers = new Headers(opts.headers || {});
  const method = (opts.method as string).toUpperCase();
  const hasBody = !!opts.body;
  const isFormData =
    typeof FormData !== "undefined" && opts.body instanceof FormData;

  // default accept
  if (!headers.has("Accept")) headers.set("Accept", "application/json");

  if (method !== "GET" && method !== "HEAD") {
    // only set content-type when we're actually sending JSON
    if (hasBody && !isFormData && !headers.has("Content-Type")) {
      headers.set("Content-Type", "application/json");
    }
    // CSRF header from cookie
    const token =
      Cookies.get("csrf_token") ||
      Cookies.get("XSRF-TOKEN") ||
      Cookies.get("csrf-token");
    if (token) headers.set("X-CSRF-Token", token);
  }

  opts.headers = headers;

  const res = await fetch(url, opts);

  // throw Response for 4xx/5xx so callers can handle
  if (res.status >= 400) throw res;

  return res; // caller decides whether to res.json(), res.text(), etc.
}