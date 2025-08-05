import Cookies from 'js-cookie';

interface CsrfFetchOptions extends RequestInit {
  headers?: HeadersInit & {
    'X-CSRF-Token'?: string;
  };
}

export async function csrfFetch(url: string, options: CsrfFetchOptions = {}) {
  options.method = options.method || 'GET';
  options.headers = options.headers || {};

  if (options.method.toUpperCase() !== 'GET') {
    if (!options.headers['Content-Type']) {
      options.headers['Content-Type'] = 'application/json';
    }

    const csrfToken = Cookies.get('csrf_token');
    if (csrfToken) {
      options.headers['X-CSRF-Token'] = csrfToken;
    }
  }

  options.credentials = 'include';

  const res = await window.fetch(url, options);

  if (res.status >= 400) throw res;

  return res;
}