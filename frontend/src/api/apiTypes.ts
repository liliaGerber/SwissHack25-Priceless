// Defines types for api responses and requests

export type APIResponse<T> = {
    success: boolean
    content: T;
    status?: number;
}