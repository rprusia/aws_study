# AWS Certified Solutions Architect - Associate: CloudFront Study Notes

Current focus: Amazon CloudFront for SAA-C03 questions involving content delivery, static and dynamic web acceleration, private origin access, caching, TLS, web security, and cost/performance tradeoffs.

## Exam Weight

CloudFront appears across multiple domains:

- Domain 1: Design Secure Architectures, especially private S3 origins, signed URLs/cookies, TLS, WAF, and origin protection.
- Domain 2: Design Resilient Architectures, especially global edge delivery and reducing origin load.
- Domain 3: Design High-Performing Architectures, especially cache hit ratio, latency reduction, and global content delivery.
- Domain 4: Design Cost-Optimized Architectures, especially cache TTLs, origin offload, price classes, invalidation cost, and data transfer patterns.

Key exam framing:

- Use CloudFront when users are geographically distributed and need low-latency delivery.
- Use CloudFront in front of S3, ALB, API Gateway, EC2, or custom HTTP origins.
- Prefer cacheable, static, repeated content at the edge.
- For private S3 origins, prefer Origin Access Control (OAC), not public buckets.
- Keep the cache key small unless the content truly varies by headers, cookies, or query strings.
- Use AWS WAF with CloudFront for edge-layer application protection.

## Core CloudFront Concepts

### Distributions

A CloudFront distribution is the main configuration object. It defines:

- Origins that contain the definitive content.
- Cache behaviors that decide how requests are routed and cached.
- Viewer protocol rules such as HTTP-to-HTTPS redirects.
- Alternate domain names and certificates.
- Logging, WAF integration, geo restrictions, and price class.

CloudFront assigns a domain such as `d111111abcdef8.cloudfront.net`. For a custom domain such as `www.example.com`, add an alternate domain name to the distribution, attach a matching certificate, and point DNS to the CloudFront distribution.

### Origins

An origin is the backend source CloudFront fetches from on a cache miss.

Common origins:

- Amazon S3 bucket origin.
- Application Load Balancer.
- API Gateway endpoint.
- EC2 instance or on-premises HTTP server.
- MediaPackage or other AWS media services.

Exam distinction:

- S3 REST endpoint origin can use OAC.
- S3 static website endpoint is treated as a custom HTTP origin and cannot use OAC or OAI.

### Edge Locations and Regional Edge Caches

CloudFront serves viewer requests from globally distributed edge locations. On a cache hit, CloudFront returns the object directly from the edge. On a cache miss, CloudFront fetches from the origin and can cache the response for future viewers.

Benefits:

- Lower viewer latency.
- Reduced origin load.
- Improved global throughput.
- More resilient delivery for cacheable content.
- AWS backbone network used for origin retrieval paths where applicable.

### Cache Behaviors

Cache behaviors map request path patterns to settings.

Examples:

- `/images/*` routes to an S3 origin with long TTLs.
- `/api/*` routes to an ALB or API Gateway with caching disabled or very short TTLs.
- Default behavior catches all paths not matched by ordered behaviors.

Ordered behaviors are evaluated by path pattern. More specific path patterns should be placed before broader ones.

## Caching and Cache Keys

### Cache Key

The cache key determines whether two viewer requests are treated as the same cached object.

The cache key can include:

- URL path.
- Selected query strings.
- Selected headers.
- Selected cookies.

High-yield rule: Include only what changes the response. A smaller cache key improves the cache hit ratio. A larger cache key can reduce stale or incorrect responses but increases cache fragmentation and origin load.

### Cache Policies

A cache policy controls:

- Which headers, cookies, and query strings are included in the cache key.
- Minimum, default, and maximum TTL.
- Whether CloudFront requests and caches compressed objects.

Use managed cache policies when they match the use case. Use custom cache policies when response variation needs are specific.

Common examples:

- Static assets: long TTL, minimal cache key, compression enabled.
- Dynamic or personalized content: caching disabled or key varies by the required identity/session values.
- API responses: short TTL only when responses are shared and safe to cache.

### Origin Request Policies

An origin request policy controls what CloudFront forwards to the origin on cache misses, without necessarily including those values in the cache key.

Important distinction:

- Cache policy: what makes cached variants unique.
- Origin request policy: what extra request data the origin receives.

If a header, cookie, or query string is included in the cache key, it is automatically forwarded to the origin. Use an origin request policy for values the origin needs but that should not fragment the cache.

### TTLs and Expiration

CloudFront uses TTL values to decide how long an object remains fresh in edge cache.

Sources of TTL:

- `Cache-Control` and `Expires` headers from the origin.
- Cache policy minimum, default, and maximum TTL.

Exam patterns:

- Static versioned files such as `app.a1b2c3.js`: long TTL.
- Frequently changing unversioned files such as `index.html`: short TTL.
- Emergency content update: use invalidation, but design with versioned filenames to avoid frequent invalidations.

### Invalidations

Invalidation removes cached objects from CloudFront before they expire.

Use invalidation when:

- Content changed but the URL did not.
- You must force CloudFront to fetch a new version before TTL expiry.

Cost/performance reminder:

- Prefer versioned object names for routine deployments.
- Use invalidation for exceptions, mistakes, or urgent updates.

## Origin Access Control and Private S3

### OAC

Origin Access Control (OAC) is the recommended way to keep an S3 bucket private while allowing CloudFront to read objects.

OAC supports:

- S3 buckets in all AWS Regions, including newer opt-in Regions.
- SSE-KMS encrypted objects.
- Dynamic S3 requests such as `PUT` and `DELETE`.

Typical private S3 pattern:

1. Create an S3 bucket with public access blocked.
2. Create a CloudFront distribution with the S3 bucket as an origin.
3. Configure OAC with signed requests.
4. Add an S3 bucket policy allowing the CloudFront service principal.
5. Restrict the bucket policy with `AWS:SourceArn` for the specific distribution.

Bucket policy pattern:

```json
{
  "Effect": "Allow",
  "Principal": {
    "Service": "cloudfront.amazonaws.com"
  },
  "Action": "s3:GetObject",
  "Resource": "arn:aws:s3:::example-bucket/*",
  "Condition": {
    "StringEquals": {
      "AWS:SourceArn": "arn:aws:cloudfront::111122223333:distribution/EXAMPLEID"
    }
  }
}
```

### OAI

Origin Access Identity (OAI) is the older S3 private-origin mechanism. For new designs, prefer OAC unless a question clearly describes an existing OAI setup or legacy constraint.

### SSE-KMS with S3 Origins

If S3 objects use SSE-KMS, CloudFront needs permission to use the KMS key. The design must include both:

- S3 bucket policy allowing CloudFront access through OAC.
- KMS key policy allowing the CloudFront distribution to decrypt the objects.

Exam trap: S3 permission alone is not enough for SSE-KMS encrypted objects.

## Signed URLs and Signed Cookies

Use signed URLs or signed cookies to restrict viewer access to private content served through CloudFront.

### Signed URLs

Use signed URLs when:

- Access is for a single object or small number of objects.
- The client can receive unique links.
- Example: paid download link for one file.

### Signed Cookies

Use signed cookies when:

- Users need access to multiple restricted objects.
- You do not want to change URLs.
- Example: subscriber access to a library of videos or lessons.

### Trusted Key Groups

Modern CloudFront private content uses public keys and trusted key groups. The application creates a signed URL or cookie with a private key, and CloudFront verifies it with the public key in the trusted key group.

Policy options:

- Canned policy: simple expiration.
- Custom policy: expiration, start time, and optional IP address restriction.

Exam distinction:

- OAC protects the origin from direct public access.
- Signed URLs/cookies control which viewers can access CloudFront content.

## TLS, HTTPS, and Custom Domains

### Viewer to CloudFront

For HTTPS with the default CloudFront domain, use the default CloudFront certificate.

For HTTPS with a custom domain:

- Add the alternate domain name to the distribution.
- Use an ACM certificate that covers the domain.
- The ACM certificate for viewer-facing CloudFront TLS must be in `us-east-1`.
- DNS should route the custom domain to the distribution, commonly with a Route 53 alias record.

### CloudFront to Origin

For custom origins, configure the origin protocol policy:

- HTTP only.
- HTTPS only.
- Match viewer.

For end-to-end encryption, require HTTPS from viewer to CloudFront and from CloudFront to origin.

Origin TLS gotcha:

- The certificate on a custom origin must match the origin domain name configured in CloudFront.
- If it does not match, CloudFront can return `502 Bad Gateway`.

### Viewer Protocol Policy

Common choices:

- Redirect HTTP to HTTPS: preferred for public websites that should support users typing `http://`.
- HTTPS only: reject HTTP viewer requests.
- HTTP and HTTPS: usually not preferred for secure content.

### SNI and Legacy Clients

Use SNI-only custom SSL for most modern clients. Dedicated IP custom SSL supports older clients but costs more and is rarely the best exam answer unless the question explicitly requires legacy non-SNI client support.

## AWS WAF and Edge Security

CloudFront integrates with AWS WAF to inspect and block malicious HTTP/S requests before they reach the origin.

Use AWS WAF for:

- OWASP Top 10 protections.
- SQL injection and cross-site scripting protections.
- IP allowlists and blocklists.
- Rate-based rules.
- Bot and abuse mitigation patterns.
- Geo-based blocking when paired with WAF rules, or use CloudFront geo restriction for simpler country allow/deny.

Exam pattern:

- "Protect a global web application from common web exploits at the edge": CloudFront plus AWS WAF.
- "Block traffic from certain countries": CloudFront geo restriction or AWS WAF, depending on rule complexity.
- "Rate limit abusive requests": AWS WAF rate-based rules.

## Global Performance Patterns

CloudFront improves performance by caching content near viewers and reducing origin round trips.

Good candidates:

- Static websites.
- Images, CSS, JavaScript, fonts, and videos.
- Downloads.
- Public APIs with shared cacheable responses.
- Dynamic applications that benefit from TLS termination, connection reuse, edge routing, and selective caching.

Less ideal candidates:

- Highly personalized responses where every user sees unique content.
- Workloads where data must never be cached and users are close to the origin.

Even with caching disabled, CloudFront can still improve performance through global edge networking, TLS termination, persistent origin connections, and request routing over AWS infrastructure.

## Cost Tradeoffs

CloudFront costs are driven by:

- Data transfer out to viewers.
- HTTP/HTTPS requests.
- Invalidation requests beyond included allowances.
- Optional features such as field-level encryption, real-time logs, WAF, and dedicated IP custom SSL.

Cost optimization patterns:

- Increase cache hit ratio to reduce origin load and origin data transfer.
- Use long TTLs with versioned file names for static assets.
- Avoid forwarding unnecessary headers, cookies, and query strings.
- Choose a price class that limits edge locations when lower cost matters more than maximum global performance.
- Use S3 plus CloudFront for static content instead of serving static assets from EC2.
- Avoid frequent broad invalidations such as `/*` during normal releases.

### Price Class

Price class controls which edge locations CloudFront uses based on cost.

General exam framing:

- All edge locations: best performance, higher cost.
- Restricted price classes: lower cost, possibly higher latency for excluded geographies.

If the question says "lowest latency globally," choose all edge locations. If it says "reduce cost and most users are in North America and Europe," choose a lower price class appropriate to those regions.

## Logging and Observability

CloudFront supports access logging for request analysis and troubleshooting.

Logging uses:

- Standard logs for request-level records.
- Real-time logs for near-real-time visibility when needed.
- CloudWatch metrics for distribution health and traffic.
- AWS WAF logs for security events when WAF is attached.

Exam patterns:

- Need request records for audits or traffic analysis: enable CloudFront logs.
- Need security rule visibility: enable AWS WAF logging.
- Need origin troubleshooting: check cache hit/miss, origin status codes, and `502` TLS/domain mismatch issues.

## Common Scenario Patterns

### Private Static Website on S3

Best answer: S3 bucket with public access blocked, CloudFront distribution, OAC, bucket policy restricted to the distribution, and HTTPS with ACM certificate if using a custom domain.

Avoid:

- Public S3 bucket.
- IAM users or access keys for viewers.
- OAI for new designs when OAC is available.

### Global Static Assets

Best answer: Store assets in S3, serve through CloudFront, use long TTLs, enable compression, and use versioned file names.

Why: CloudFront reduces latency and origin load, and versioned file names avoid repeated invalidations.

### Dynamic API Behind ALB

Best answer: CloudFront in front of ALB with cache behaviors for API paths. Cache only safe shared responses, forward required headers/query strings, and use HTTPS.

Why: You can accelerate global access without incorrectly caching personalized responses.

### Personalized Content

Best answer: Do not cache or cache carefully by the values that truly change the response, such as selected cookies or authorization-related headers when appropriate.

Why: Incorrect cache keys can leak personalized content between users.

### Paid Video or Download Access

Best answer: Use CloudFront signed URLs for individual files or signed cookies for access to many restricted files.

Why: Signed URLs/cookies restrict viewer access at CloudFront. OAC alone only protects the origin.

### Protect Origin from Web Attacks

Best answer: Put CloudFront in front of the origin and attach AWS WAF web ACL with managed and custom rules.

Why: AWS WAF blocks malicious requests before they reach the origin.

### Require HTTPS on Custom Domain

Best answer: Request or import an ACM certificate in `us-east-1`, attach it to the distribution, add the alternate domain name, configure DNS, and use redirect HTTP to HTTPS or HTTPS only.

### Origin Returns 502 After Enabling HTTPS

Likely cause: Custom origin TLS certificate does not match the origin domain name configured in CloudFront, is expired, or is not trusted.

Best answer: Fix the origin certificate or origin domain name.

### Reduce Cost for Regional Audience

Best answer: Use an appropriate CloudFront price class, improve cache hit ratio, use long TTLs for static assets, and avoid unnecessary cache key variation.

## High-Yield Exam Reminders

- CloudFront is a global content delivery network.
- A distribution has origins and cache behaviors.
- Default cache behavior applies when no ordered behavior matches.
- S3 REST origins can use OAC; S3 website endpoints are custom origins and cannot use OAC.
- OAC is recommended over OAI for new private S3 designs.
- OAC protects the origin; signed URLs/cookies protect viewer access.
- Cache policy controls cache key and TTLs.
- Origin request policy controls what CloudFront forwards to the origin on misses.
- Fewer cache key values usually means better cache hit ratio.
- Do not forward all cookies/headers/query strings unless required.
- Use versioned file names for deployments; use invalidation for urgent or unversioned changes.
- ACM certificates for viewer-facing CloudFront custom domains must be in `us-east-1`.
- Custom origin certificates must match the configured origin domain name.
- Use AWS WAF with CloudFront for web exploit protection and rate limiting.
- Use price classes to trade global performance for lower cost.
- Use Route 53 alias records for apex domains pointing to CloudFront.
- Dedicated IP custom SSL is for legacy non-SNI clients and costs more.

## Practice Questions

### 1. Private S3 Content

A company wants to serve private S3 objects globally through CloudFront. Users must not be able to bypass CloudFront and access S3 directly. What should be configured?

Answer: Use CloudFront with Origin Access Control, keep the S3 bucket private with public access blocked, and add a bucket policy allowing the CloudFront service principal only from the distribution ARN.

Why: OAC allows CloudFront to securely access the S3 origin while preventing direct public S3 access.

### 2. Custom Domain HTTPS

A CloudFront distribution must serve `www.example.com` over HTTPS. Where must the ACM certificate be created?

Answer: `us-east-1`.

Why: Viewer-facing ACM certificates for CloudFront custom domains must be requested or imported in US East (N. Virginia).

### 3. Cache Hit Ratio

A CloudFront distribution forwards all headers, cookies, and query strings for static image files. The origin is overloaded and cache hit ratio is low. What should be changed?

Answer: Use a cache policy that includes only values that actually change the image response, likely none for static images, and use long TTLs.

Why: Excessive cache key variation fragments the cache and increases origin requests.

### 4. Paid Downloads

Users who purchase a file should receive temporary access to download it through CloudFront. Which feature should be used?

Answer: CloudFront signed URLs.

Why: Signed URLs are suitable for temporary access to individual private objects.

### 5. Subscriber Video Library

Authenticated subscribers need access to many video files without changing each URL. Which feature should be used?

Answer: CloudFront signed cookies.

Why: Signed cookies grant controlled access to multiple restricted objects while keeping normal URLs.

### 6. Web Exploit Protection

A public web application behind CloudFront must be protected from SQL injection, cross-site scripting, and abusive request rates. What should be added?

Answer: AWS WAF web ACL associated with the CloudFront distribution, using managed rules and rate-based rules.

Why: AWS WAF inspects and blocks malicious requests at the edge before they reach the origin.

### 7. Cost vs Global Reach

Most users are in North America and Europe. The company wants to reduce CDN cost and accepts slightly higher latency elsewhere. What should be considered?

Answer: Use a lower CloudFront price class that focuses on the required geographies.

Why: Price classes trade edge-location coverage for lower cost.

### 8. Stale Static Asset After Deployment

A JavaScript file changed but users still receive the old file from CloudFront. The application uses the same filename. What are two valid fixes?

Answer: Invalidate the object in CloudFront or deploy the file with a new versioned filename.

Why: Invalidation forces refresh for the current URL; versioned filenames are the better routine deployment pattern.

## Sources

- Amazon CloudFront Developer Guide: https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/Introduction.html
- Cache policies: https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/controlling-the-cache-key.html
- Origin request policies: https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/controlling-origin-requests.html
- Restrict access to an S3 origin with OAC: https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/private-content-restricting-access-to-s3.html
- Signed URLs: https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/private-content-signed-urls.html
- Signed cookies: https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/private-content-signed-cookies.html
- AWS WAF with CloudFront: https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/distribution-web-awswaf.html
- TLS certificate requirements: https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/cnames-and-https-requirements.html
- Distribution settings: https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/DownloadDistValuesGeneral.html
- Cache expiration: https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/Expiration.html
