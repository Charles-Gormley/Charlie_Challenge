package main

import (
	"crypto/tls"
	"fmt"
	"flag"
	"net/http"
	"testing"
)

// Configure the domain name to test via command line flag. This is set inside deploy.py
var domainName = flag.String("domain", "www.google.com", "The domain name to test")


// TestHttpsAccessibility checks if the site is accessible over HTTPS and validates the HTTP status code is 200 OK.
func TestHttpsAccessibility(t *testing.T) {
	// Skip TLS verification for the test
	http.DefaultTransport.(*http.Transport).TLSClientConfig = &tls.Config{InsecureSkipVerify: true}

	resp, err := http.Get("https://" + *domainName)
	if err != nil {
		t.Fatalf("HTTPS Accessibility: Failed - Unable to access site via HTTPS: %v", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode == http.StatusOK {
		fmt.Println("HTTPS Accessibility: Passed")
	} else {
		t.Errorf("HTTPS Accessibility: Failed - Expected HTTP status code 200, got: %d", resp.StatusCode)
	}
}

// TestHttpToHttpsRedirection checks if HTTP requests are redirected to HTTPS, expecting a 301 Moved Permanently or 302 Found status code.
func TestHttpToHttpsRedirection(t *testing.T) {

	resp, err := http.Get("http://" + *domainName)
	if err != nil {
		t.Fatalf("HTTP to HTTPS Redirection: Failed - Unable to access site via HTTP: %v", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode == http.StatusMovedPermanently || resp.StatusCode == http.StatusFound || resp.StatusCode == http.StatusOK {
		fmt.Println("HTTP to HTTPS Redirection: Passed")
	} else {
		t.Errorf("HTTP to HTTPS Redirection: Failed - Expected HTTP status code for redirection (301 or 302), got: %d", resp.StatusCode)
	}
}
