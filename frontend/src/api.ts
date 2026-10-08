const API_BASE = import.meta.env.VITE_API_BASE_URL || "/api";

export type UserOut = {
  id?: number;
  username: string;
  display_name?: string;
  role: string;
  relationship_label?: string | null;
};

export type LoginResponse = {
  ok: boolean;
  user: UserOut;
};

export async function api<T>(path: string, options: RequestInit = {}): Promise<T> {
  const headers = new Headers(options.headers);

  if (options.body && !headers.has("Content-Type")) {
    headers.set("Content-Type", "application/json");
  }

  const response = await fetch(`${API_BASE}${path}`, {
    ...options,
    credentials: "include",
    headers,
  });

  if (!response.ok) {
    let message = `Ошибка ${response.status}`;

    try {
      const data = await response.json();
      message = data.detail || data.message || JSON.stringify(data);
    } catch {
      // ignore
    }

    throw new Error(message);
  }

  return response.json() as Promise<T>;
}