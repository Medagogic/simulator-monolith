# Decision Record 0007: Codegen for SocketIO
- We will try to use some automatic codegen to help with type safety and code completion for our SocketIO communication.
- This exists inside the tools package, and uses a combination of stuff to work
- It relies on some fancy introspective code though which is a bit nasty