#!/usr/bin/env python3
"""Build NHS-styled API documentation using RapiDoc, matching digital.nhs.uk layout."""

import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SPEC_FILE = os.path.join(ROOT, "specification", "validated-relationships-service-api.yaml")
BUILD_DIR = os.path.join(ROOT, "build")
BUNDLE_FILE = os.path.join(BUILD_DIR, "spec-bundled.json")
OUTPUT = os.path.join(BUILD_DIR, "docs.html")

NHS_CATALOGUE_URL = "https://digital.nhs.uk/developer/api-catalogue/validated-relationship-service"


def fetch_nhs_js_files():
    """Download NHS Digital's exact rapidoc-min.js and rapidoc-customisation.js using curl."""
    print("Fetching NHS Digital page to find current JS version...")
    result = subprocess.run(
        ["curl", "-s", NHS_CATALOGUE_URL],
        capture_output=True,
        text=True,
    )
    match = re.search(r"/webfiles/(\d+)/apispecification/rapidoc-min\.js", result.stdout)
    if not match:
        sys.exit("Could not find rapidoc JS URL on NHS Digital page")
    version = match.group(1)

    version_marker = os.path.join(BUILD_DIR, ".js_version")
    if os.path.exists(version_marker):
        with open(version_marker) as f:
            cached_version = f.read().strip()
    else:
        cached_version = ""

    base = f"https://digital.nhs.uk/webfiles/{version}/apispecification"
    for filename in ("rapidoc-min.js", "rapidoc-customisation.js"):
        dest = os.path.join(BUILD_DIR, filename)
        if os.path.exists(dest) and cached_version == version:
            print(f"  {filename} already up to date (version {version})")
            continue
        url = f"{base}/{filename}"
        print(f"  Downloading {url}")
        subprocess.run(["curl", "-s", url, "-o", dest], check=True)

    with open(version_marker, "w") as f:
        f.write(version)
    return version


def bundle_spec():
    print("Bundling spec to JSON...")
    result = subprocess.run(
        [
            "npx",
            "--yes",
            "@redocly/cli",
            "bundle",
            SPEC_FILE,
            "--output",
            BUNDLE_FILE,
            "--ext",
            "json",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print("Error bundling spec:\n", result.stderr, file=sys.stderr)
        sys.exit(1)
    with open(BUNDLE_FILE) as f:
        return f.read()


def generate_html(spec_json, js_version):
    title = "Validated Relationship Service - FHIR API"

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title} — LOCALDEV PREVIEW</title>

  <!-- Frutiger W01 -->
  <style>
    @font-face {{
      font-family: 'Frutiger W01';
      font-weight: 300;
      src: url('https://design-system.digital.nhs.uk/cdn/latest/fonts/FrutigerLTW01-45Light.woff2') format('woff2');
    }}
    @font-face {{
      font-family: 'Frutiger W01';
      font-weight: 400;
      src: url('https://design-system.digital.nhs.uk/cdn/latest/fonts/FrutigerLTW01-55Roman.woff2') format('woff2');
    }}
    @font-face {{
      font-family: 'Frutiger W01';
      font-weight: 600;
      src: url('https://design-system.digital.nhs.uk/cdn/latest/fonts/FrutigerLTW01-65Bold.woff2') format('woff2');
    }}
  </style>

  <!-- NHS Design System CSS (sets 18px root, nhsd-* classes) -->
  <link rel="stylesheet" href="https://design-system.digital.nhs.uk/cdn/latest/stylesheets/nhsd-frontend.css">

  <!--
    NHS Digital's exact RapiDoc JS (version {js_version}) — downloaded locally.
    rapidoc-customisation.js handles loadSpec(specification) itself.
  -->
  <script src="rapidoc-min.js"></script>
  <script src="rapidoc-customisation.js"></script>

  <style>
    body {{ margin: 0; padding: 0; }}

    /* ── Simplified NHS header ── */
    .preview-header {{ background: #005eb8; }}
    .preview-header__inner {{
      width: 100%;
      max-width: 38.222rem;
      margin: 0 auto;
      padding: 0 0.833rem;
      display: flex;
      align-items: center;
      height: 56px;
      box-sizing: border-box;
    }}
    @media (min-width: 64em)     {{ .preview-header__inner {{ max-width: 52.444rem; }} }}
    @media (min-width: 77.5em)   {{ .preview-header__inner {{ max-width: 58.888rem; }} }}
    @media (min-width: 85.375em) {{ .preview-header__inner {{ max-width: 71.111rem; }} }}
    @media (min-width: 98.75em)  {{ .preview-header__inner {{ max-width: 83.333rem; }} }}
    .preview-header__logo {{ display: flex; align-items: center; text-decoration: none; }}
    .preview-header__logo svg {{ height: 1.556rem; fill: #fff; }}
    .preview-header__divider {{
      width: 1px; height: 1.556rem;
      background: rgba(255,255,255,0.4);
      margin: 0 1.111rem; flex-shrink: 0;
    }}
    .preview-header__name {{
      color: #fff;
      font-family: 'Frutiger W01', Arial, sans-serif;
      font-size: 1.056rem; font-weight: 600;
    }}
    .preview-header__nav {{ margin-left: auto; display: flex; gap: 1.333rem; }}
    .preview-header__nav a {{
      color: rgba(255,255,255,0.9);
      font-family: 'Frutiger W01', Arial, sans-serif;
      font-size: 0.889rem; text-decoration: none;
    }}
    .preview-header__nav a:hover {{ text-decoration: underline; }}

    /* ── RapiDoc — same inline styles as digital.nhs.uk ── */
    .rapi-doc-component {{ overflow: unset; }}
    rapi-doc::part(section-navbar-search) {{
      justify-content: flex-start; padding: 0; margin-bottom: 15px;
    }}
    rapi-doc::part(btn-search) {{ margin: 0; width: unset; }}
    rapi-doc::part(btn-try) {{ margin: 16px 5px 0 0; }}
    rapi-doc::part(wrap-request-btn) {{
      flex-direction: row-reverse; flex-wrap: wrap;
      justify-content: flex-end; padding-top: 12px;
    }}
  </style>
</head>
<body>
  <!-- Breadcrumb — exact structure from digital.nhs.uk -->
  <div class="nhsd-t-grid nhsd-!t-padding-top-3 nhsd-!t-padding-bottom-3">
    <div class="nhsd-t-row">
      <div class="nhsd-t-col">
        <nav class="nhsd-m-breadcrumbs" aria-label="Breadcrumbs">
          <ol class="nhsd-m-breadcrumbs__list">
            <li class="nhsd-m-breadcrumbs__item">
              <a class="nhsd-a-link nhsd-a-link--col-dark-grey" href="https://digital.nhs.uk">NHS Digital</a>
              <span class="nhsd-a-icon nhsd-a-icon--size-xxs nhsd-a-icon--col-dark-grey" aria-hidden="true">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" width="100%" height="100%">
                  <path d="M12,8l-6.5,7L4,13.5L9.2,8L4,2.5L5.5,1L12,8z"/>
                </svg>
              </span>
            </li>
            <li class="nhsd-m-breadcrumbs__item">
              <a class="nhsd-a-link nhsd-a-link--col-dark-grey" href="https://digital.nhs.uk/developer">Developer</a>
              <span class="nhsd-a-icon nhsd-a-icon--size-xxs nhsd-a-icon--col-dark-grey" aria-hidden="true">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" width="100%" height="100%">
                  <path d="M12,8l-6.5,7L4,13.5L9.2,8L4,2.5L5.5,1L12,8z"/>
                </svg>
              </span>
            </li>
            <li class="nhsd-m-breadcrumbs__item">
              <a class="nhsd-a-link nhsd-a-link--col-dark-grey"
                href="https://digital.nhs.uk/developer/api-catalogue"
              >API and integration catalogue</a>
              <span class="nhsd-a-icon nhsd-a-icon--size-xxs nhsd-a-icon--col-dark-grey" aria-hidden="true">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" width="100%" height="100%">
                  <path d="M12,8l-6.5,7L4,13.5L9.2,8L4,2.5L5.5,1L12,8z"/>
                </svg>
              </span>
            </li>
            <li class="nhsd-m-breadcrumbs__item">
              <span class="nhsd-t-body-s" aria-current="page">{title}</span>
            </li>
          </ol>
        </nav>
      </div>
    </div>
  </div>

  <!-- Hero — exact structure from digital.nhs.uk -->
  <div class="nhsd-o-hero nhsd-o-hero--left-align nhsd-!t-text-align-left">
    <div class="nhsd-o-hero__content-container">
      <div class="nhsd-o-hero__inner-content-container">
        <h1 class="nhsd-t-heading-xxl nhsd-!t-margin-bottom-0">{title}</h1>
        <div class="nhsd-t-body nhsd-!t-margin-top-6 nhsd-!t-margin-bottom-0">
          <p>
            This is a LOCALDEV PREVIEW of the API documentation for the Validated Relationships Service.
            It is intended for use during development to view the API documentation in a format SIMILAR TO the
            <a href="https://digital.nhs.uk/developer/api-catalogue/validated-relationship-service"
              target="_blank">NHS Digital API catalogue</a>.
          </p>
          <p>
            Although the layout of this preview is not exact, it should provide confidence to developers
            that any changes made to the OpenAPI specification will be reflected in the final published spec.
          </p>
        </div>
        <nav class="nhsd-m-button-nav nhsd-m-button-nav--condensed nhsd-!t-text-align-left nhsd-!t-margin-top-6">
          <a class="nhsd-a-button" href="spec-bundled.json" target="_blank">
            <span class="nhsd-a-button__label">Get OAS file</span>
          </a>
        </nav>
      </div>
    </div>
    <div class="nhsd-a-digiblocks nhsd-a-digiblocks--pos-tr">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 550 550">
        <g>
          <g transform="translate(222, 224)">
            <polygon points="0,20.5 35.5,0 71,20.5 35.5,41" fill="#BFD7ED"></polygon>
            <polygon points="35.5,82 71,61.4 71,20.5 35.5,41" fill="#B2CFEA"></polygon>
            <polygon points="0,20.5 0,61.4 35.5,82 35.5,41" fill="#A6C7E6"></polygon>
          </g>
          <g transform="translate(328.5, 367.5)">
            <polygon points="0,20.5 35.5,0 71,20.5 35.5,41" fill="#FBFAFA"></polygon>
            <polygon points="35.5,82 71,61.4 71,20.5 35.5,41" fill="#F5F5F4"></polygon>
            <polygon points="0,20.5 0,61.4 35.5,82 35.5,41" fill="#EFF2F1"></polygon>
          </g>
          <g transform="translate(151, 306)">
            <polygon points="0,20.5 35.5,0 71,20.5 35.5,41" fill="#3C4D57"></polygon>
            <polygon points="35.5,82 71,61.4 71,20.5 35.5,41" fill="#32434C"></polygon>
            <polygon points="0,20.5 0,61.4 35.5,82 35.5,41" fill="#313D45"></polygon>
          </g>
          <g transform="translate(80, 306)">
            <polygon points="0,20.5 35.5,0 71,20.5 35.5,41" fill="#FBFAFA"></polygon>
            <polygon points="35.5,82 71,61.4 71,20.5 35.5,41" fill="#F5F5F4"></polygon>
            <polygon points="0,20.5 0,61.4 35.5,82 35.5,41" fill="#EFF2F1"></polygon>
          </g>
        </g>
        <g>
          <g transform="translate(186.5, 203.5)">
            <polygon points="0,20.5 35.5,0 71,20.5 35.5,41" fill="#FBFAFA"></polygon>
            <polygon points="35.5,82 71,61.4 71,20.5 35.5,41" fill="#F5F5F4"></polygon>
            <polygon points="0,20.5 0,61.4 35.5,82 35.5,41" fill="#EFF2F1"></polygon>
          </g>
          <g transform="translate(186.5, 285.5)">
            <polygon points="0,20.5 35.5,0 71,20.5 35.5,41" fill="#00267A"></polygon>
            <polygon points="35.5,82 71,61.4 71,20.5 35.5,41" fill="#001F75"></polygon>
            <polygon points="0,20.5 0,61.4 35.5,82 35.5,41" fill="#001766"></polygon>
          </g>
          <g transform="translate(222, 306)">
            <polygon points="0,20.5 35.5,0 71,20.5 35.5,41" fill="#00267A"></polygon>
            <polygon points="35.5,82 71,61.4 71,20.5 35.5,41" fill="#001F75"></polygon>
            <polygon points="0,20.5 0,61.4 35.5,82 35.5,41" fill="#001766"></polygon>
          </g>
          <g transform="translate(9, 306)">
            <polygon points="0,20.5 35.5,0 71,20.5 35.5,41" fill="#00267A"></polygon>
            <polygon points="35.5,82 71,61.4 71,20.5 35.5,41" fill="#001F75"></polygon>
            <polygon points="0,20.5 0,61.4 35.5,82 35.5,41" fill="#001766"></polygon>
          </g>
          <g transform="translate(257.5, 449.5)">
            <polygon points="0,20.5 35.5,0 71,20.5 35.5,41" fill="#F5D507"></polygon>
            <polygon points="35.5,82 71,61.4 71,20.5 35.5,41" fill="#F2CB0C"></polygon>
            <polygon points="0,20.5 0,61.4 35.5,82 35.5,41" fill="#EEC000"></polygon>
          </g>
        </g>
        <g>
          <g transform="translate(186.5, 203.5)">
            <polygon points="0,20.5 35.5,0 71,20.5 35.5,41" fill="#6D7B86"></polygon>
            <polygon points="35.5,82 71,61.4 71,20.5 35.5,41" fill="#62717A"></polygon>
            <polygon points="0,20.5 0,61.4 35.5,82 35.5,41" fill="#5C6B75"></polygon>
          </g>
          <g transform="translate(399.5, 326.5)">
            <polygon points="0,20.5 35.5,0 71,20.5 35.5,41" fill="#BFD7ED"></polygon>
            <polygon points="35.5,82 71,61.4 71,20.5 35.5,41" fill="#B2CFEA"></polygon>
            <polygon points="0,20.5 0,61.4 35.5,82 35.5,41" fill="#A6C7E6"></polygon>
          </g>
          <g transform="translate(222, 306)">
            <polygon points="0,20.5 35.5,0 71,20.5 35.5,41" fill="#FBFAFA"></polygon>
            <polygon points="35.5,82 71,61.4 71,20.5 35.5,41" fill="#F5F5F4"></polygon>
            <polygon points="0,20.5 0,61.4 35.5,82 35.5,41" fill="#EFF2F1"></polygon>
          </g>
        </g>
        <g>
          <g transform="translate(328.5, 162.5)">
            <polygon points="0,20.5 35.5,0 71,20.5 35.5,41" fill="#F5D507"></polygon>
            <polygon points="35.5,82 71,61.4 71,20.5 35.5,41" fill="#F2CB0C"></polygon>
            <polygon points="0,20.5 0,61.4 35.5,82 35.5,41" fill="#EEC000"></polygon>
          </g>
          <g transform="translate(399.5, 244.5)">
            <polygon points="0,20.5 35.5,0 71,20.5 35.5,41" fill="#00267A"></polygon>
            <polygon points="35.5,82 71,61.4 71,20.5 35.5,41" fill="#001F75"></polygon>
            <polygon points="0,20.5 0,61.4 35.5,82 35.5,41" fill="#001766"></polygon>
          </g>
          <g transform="translate(115.5, 162.5)">
            <polygon points="0,20.5 35.5,0 71,20.5 35.5,41" fill="#6D7B86"></polygon>
            <polygon points="35.5,82 71,61.4 71,20.5 35.5,41" fill="#62717A"></polygon>
            <polygon points="0,20.5 0,61.4 35.5,82 35.5,41" fill="#5C6B75"></polygon>
          </g>
          <g transform="translate(186.5, 244.5)">
            <polygon points="0,20.5 35.5,0 71,20.5 35.5,41" fill="#0062CC"></polygon>
            <polygon points="35.5,82 71,61.4 71,20.5 35.5,41" fill="#005ABE"></polygon>
            <polygon points="0,20.5 0,61.4 35.5,82 35.5,41" fill="#0050B5"></polygon>
          </g>
          <g transform="translate(328.5, 326.5)">
            <polygon points="0,20.5 35.5,0 71,20.5 35.5,41" fill="#0062CC"></polygon>
            <polygon points="35.5,82 71,61.4 71,20.5 35.5,41" fill="#005ABE"></polygon>
            <polygon points="0,20.5 0,61.4 35.5,82 35.5,41" fill="#0050B5"></polygon>
          </g>
          <g transform="translate(257.5, 326.5)">
            <polygon points="0,20.5 35.5,0 71,20.5 35.5,41" fill="#3C4D57"></polygon>
            <polygon points="35.5,82 71,61.4 71,20.5 35.5,41" fill="#32434C"></polygon>
            <polygon points="0,20.5 0,61.4 35.5,82 35.5,41" fill="#313D45"></polygon>
          </g>
        </g>
        <g>
          <g transform="translate(328.5, 244.5)">
            <polygon points="0,20.5 35.5,0 71,20.5 35.5,41" fill="#DADFDF"></polygon>
            <polygon points="35.5,82 71,61.4 71,20.5 35.5,41" fill="#CDD5D6"></polygon>
            <polygon points="0,20.5 0,61.4 35.5,82 35.5,41" fill="#C5CDCF"></polygon>
          </g>
          <g transform="translate(257.5, 285.5)">
            <polygon points="0,20.5 35.5,0 71,20.5 35.5,41" fill="#0062CC"></polygon>
            <polygon points="35.5,82 71,61.4 71,20.5 35.5,41" fill="#005ABE"></polygon>
            <polygon points="0,20.5 0,61.4 35.5,82 35.5,41" fill="#0050B5"></polygon>
          </g>
          <g transform="translate(44.5, 203.5)">
            <polygon points="0,20.5 35.5,0 71,20.5 35.5,41" fill="#6D7B86"></polygon>
            <polygon points="35.5,82 71,61.4 71,20.5 35.5,41" fill="#62717A"></polygon>
            <polygon points="0,20.5 0,61.4 35.5,82 35.5,41" fill="#5C6B75"></polygon>
          </g>
          <g transform="translate(151, 265)">
            <polygon points="0,20.5 35.5,0 71,20.5 35.5,41" fill="#BFD7ED"></polygon>
            <polygon points="35.5,82 71,61.4 71,20.5 35.5,41" fill="#B2CFEA"></polygon>
            <polygon points="0,20.5 0,61.4 35.5,82 35.5,41" fill="#A6C7E6"></polygon>
          </g>
        </g>
        <g>
          <g transform="translate(435, 142)">
            <polygon points="0,20.5 35.5,0 71,20.5 35.5,41" fill="#0062CC"></polygon>
            <polygon points="35.5,82 71,61.4 71,20.5 35.5,41" fill="#005ABE"></polygon>
            <polygon points="0,20.5 0,61.4 35.5,82 35.5,41" fill="#0050B5"></polygon>
          </g>
        </g>
        <g>
          <g transform="translate(328.5, 39.5)">
            <polygon points="0,20.5 35.5,0 71,20.5 35.5,41" fill="#BFD7ED"></polygon>
            <polygon points="35.5,82 71,61.4 71,20.5 35.5,41" fill="#B2CFEA"></polygon>
            <polygon points="0,20.5 0,61.4 35.5,82 35.5,41" fill="#A6C7E6"></polygon>
          </g>
          <g transform="translate(222, 19)">
            <polygon points="0,20.5 35.5,0 71,20.5 35.5,41" fill="#00267A"></polygon>
            <polygon points="35.5,82 71,61.4 71,20.5 35.5,41" fill="#001F75"></polygon>
            <polygon points="0,20.5 0,61.4 35.5,82 35.5,41" fill="#001766"></polygon>
          </g>
          <g transform="translate(257.5, 80.5)">
            <polygon points="0,20.5 35.5,0 71,20.5 35.5,41" fill="#DADFDF"></polygon>
            <polygon points="35.5,82 71,61.4 71,20.5 35.5,41" fill="#CDD5D6"></polygon>
            <polygon points="0,20.5 0,61.4 35.5,82 35.5,41" fill="#C5CDCF"></polygon>
          </g>
        </g>
      </svg>
    </div>
  </div>

  <!-- RapiDoc — exact structure from digital.nhs.uk -->
  <div class="nhsd-t-grid nhsd-!t-display-no-js-hide">
    <div class="nhsd-t-row">
      <rapi-doc
        class="rapi-doc-component nhsd-!t-margin-top-6"
        id="rapi-doc-spec"
        theme="light"
        bg-color="#ffffff"
        text-color="#3f525f"
        primary-color="#005bbb"
        regular-font="Frutiger W01, Arial, sans-serif"
        load-fonts="false"
        font-size="largest"
        nav-bg-color="#ffffff"
        nav-text-color="#3f525f"
        info-description-headings-in-navbar="true"
        show-header="false"
        allow-search="false"
        allow-advanced-search="true"
        allow-server-selection="false"
        schema-description-expanded="true"
        render-style="focused"
        sort-endpoints-by="none"
        show-curl-before-try="true"
        do-api-catalogue-nav-bar-tweaks="true">
        <div slot="footer">
          <p class="nhsd-t-body nhsd-!t-margin-top-3">
            <a class="nhsd-a-link" href="#">Back to top</a>
          </p>
        </div>
      </rapi-doc>
    </div>
  </div>

  <!-- Footer -->
  <footer class="nhsd-o-global-footer" role="contentinfo">
    <div class="nhsd-t-grid">
      <div class="nhsd-t-row">
        <div class="nhsd-t-col-12">
          <div class="nhsd-t-grid nhsd-t-grid--nested">
            <div class="nhsd-t-row">
              <div class="nhsd-t-col-xs-12 nhsd-t-col-s-6 nhsd-t-col-l-3 nhsd-!t-margin-bottom-4">
                <nav aria-labelledby="footer-developer">
                  <div id="footer-developer" class="nhsd-t-body-s"><h2 class="nhsd-t-heading-m">Developer</h2></div>
                  <ul class="nhsd-t-list nhsd-t-list--links">
                    <li class="nhsd-t-body-s"><a class="nhsd-a-link nhsd-a-link--col-dark-grey"
                      href="https://digital.nhs.uk/developer/api-catalogue">API catalogue</a></li>
                    <li class="nhsd-t-body-s"><a class="nhsd-a-link nhsd-a-link--col-dark-grey"
                      href="https://digital.nhs.uk/developer/guides-and-documentation"
                    >Guides and documentation</a></li>
                    <li class="nhsd-t-body-s"><a class="nhsd-a-link nhsd-a-link--col-dark-grey"
                      href="https://digital.nhs.uk/developer/help-and-support">Help and support</a></li>
                  </ul>
                </nav>
              </div>
              <div class="nhsd-t-col-xs-12 nhsd-t-col-s-6 nhsd-t-col-l-3 nhsd-!t-margin-bottom-4">
                <nav aria-labelledby="footer-legal">
                  <div id="footer-legal" class="nhsd-t-body-s"><h2 class="nhsd-t-heading-m">Legal</h2></div>
                  <ul class="nhsd-t-list nhsd-t-list--links">
                    <li class="nhsd-t-body-s"><a class="nhsd-a-link nhsd-a-link--col-dark-grey"
                      href="https://digital.nhs.uk/about-nhs-digital/privacy-and-cookies"
                    >Privacy and cookies</a></li>
                    <li class="nhsd-t-body-s"><a class="nhsd-a-link nhsd-a-link--col-dark-grey"
                      href="https://digital.nhs.uk/about-nhs-digital/terms-and-conditions"
                    >Terms and conditions</a></li>
                    <li class="nhsd-t-body-s"><a class="nhsd-a-link nhsd-a-link--col-dark-grey"
                      href="https://digital.nhs.uk/about-nhs-digital/accessibility"
                    >Accessibility</a></li>
                  </ul>
                </nav>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </footer>

  <script>
    // rapidoc-customisation.js reads these globals and calls rapiDocEl.loadSpec(specification)
    const specification = {spec_json};
    const isDevEnv = false;

    // nhsd-frontend.css can't pierce the shadow DOM boundary, so inject the rules that
    // rapidoc-customisation.js relies on (tables, horizontal rules) directly into the shadow.
    document.addEventListener('DOMContentLoaded', () => {{
      const rapiDocEl = document.getElementById('rapi-doc-spec');
      rapiDocEl.addEventListener('spec-loaded', () => {{
        setTimeout(() => {{
          const shadow = rapiDocEl.shadowRoot;
          if (!shadow) return;
          const style = document.createElement('style');
          style.textContent = [
            // Mobile list is never needed in a local desktop preview — hide it
            '.nhsd-m-table__mobile-list {{ display: none !important; }}',
            // Restore the table which gets nhsd-!t-display-hide added to it
            '.nhsd-\\\\!t-display-hide {{ display: revert !important; }}',
            // nhsd-a-horizontal-rule styles from nhsd-frontend.css can't pierce the shadow DOM
            '.nhsd-a-horizontal-rule {{ width: 100%; height: 0; border: 0; '
            + 'border-bottom: 1px solid #d5dade; margin: 1.6666666667rem 0; }}',
          ].join('\\n');
          shadow.appendChild(style);
        }}, 100);
      }});
    }});
  </script>

</body>
</html>"""


def main():
    os.makedirs(BUILD_DIR, exist_ok=True)
    js_version = fetch_nhs_js_files()
    spec_json = bundle_spec()
    html = generate_html(spec_json, js_version)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Built: {OUTPUT}")


if __name__ == "__main__":
    main()
