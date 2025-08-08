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

  // Normalize headers
  const headers = new Headers(opts.headers || {});
  const isGet = (opts.method as string).toUpperCase() === "GET";

  if (!isGet) {
    // Don't force JSON for FormData
    const isFormData = typeof FormData !== "undefined" && opts.body instanceof FormData;
    if (!isFormData && !headers.has("Content-Type")) {
      headers.set("Content-Type", "application/json");
    }

    // Be flexible on cookie name
    const token =
      Cookies.get("csrf_token") ||
      Cookies.get("XSRF-TOKEN") ||
      Cookies.get("csrf-token");
    if (token) headers.set("X-CSRF-Token", token);
  }

  opts.headers = headers;

  const res = await window.fetch(url, opts);
  if (res.status >= 400) throw res;
  return res;
}