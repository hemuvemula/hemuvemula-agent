package proxy

// Package proxy provides a minimal HTTP client for interacting with the
// Python agent service.

import (
    "bytes"
    "context"
    "encoding/json"
    "fmt"
    "net/http"
    "time"
)

// Client wraps http.Client with base URL information.
type Client struct {
    HTTP    *http.Client
    BaseURL string
}

// NewClient creates a new proxy client with sensible defaults.
func NewClient(baseURL string) *Client {
    return &Client{
        HTTP: &http.Client{Timeout: 10 * time.Second},
        BaseURL: baseURL,
    }
}

// PostJSON sends a POST request with a JSON body to the Python agent and
// decodes the JSON response into *out*.
func (c *Client) PostJSON(ctx context.Context, path string, payload any, out any) error {
    body, err := json.Marshal(payload)
    if err != nil {
        return err
    }
    req, err := http.NewRequestWithContext(ctx, http.MethodPost, c.BaseURL+path, bytes.NewReader(body))
    if err != nil {
        return err
    }
    req.Header.Set("Content-Type", "application/json")
    resp, err := c.HTTP.Do(req)
    if err != nil {
        return err
    }
    defer resp.Body.Close()
    if resp.StatusCode >= 400 {
        return fmt.Errorf("unexpected status %d", resp.StatusCode)
    }
    return json.NewDecoder(resp.Body).Decode(out)
}
