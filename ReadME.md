# 99-OTPs

> "Because apparently, passwords alone weren't stressful enough."

A custom OTP generator for your apps. Because you deserve to make your users open their SMS app, squint at a 6-digit code, switch back to your app, and type it in — all in under 2 minutes before it self-destructs like a spy movie.

---

## What's in the box

### REST API — Python
For those of you who like your requests HTTP and your responses JSON. Clean, async, and it actually works — which is more than we can say for most side projects.

Full documentation included. You're welcome.

> "Feel free." — Isaac, probably wearing sunglasses when he said this.

### gRPC — Go
For the enlightened ones. The ones who looked at REST and said *"this isn't fast enough for my trust issues."*

Written in Go, because if you're going fast, you might as well go **really** fast. Goroutines don't sleep. Neither does this service.

Stay tuned. Good things come to those who wait — unlike OTPs, which expire in 2 minutes and take your patience with them.

Full documentation will be included. Probably.

---

## How it works

1. User tries to log in
2. You call this service
3. User's phone buzzes
4. User squints at a 6-digit code like it's ancient scripture
5. User types it in, probably wrong the first time
6. You call this service again
7. Either it works or it expired and now everyone is stressed
8. Authentication achieved. Democracy saved.

---

## Why OTPs?

Because "password123" wasn't cutting it anymore and your users refuse to use a password manager. We don't judge. We just send the code.

---

## License

MIT — meaning you can use this freely, just don't forget where you got it from.  
That's literally the only rule. Isaac just wants credit. Is that so much to ask?

---

## Contributing

Found a bug? Open an issue.  
Fixed a bug? Open a PR.  
Broke something? Pretend it was always like that and open a PR anyway.

---

*REST API built with FastAPI, Redis, httpx, and an unreasonable amount of determination.*  
*gRPC implementation written in Go — because some of us have standards. Coming soon.*
