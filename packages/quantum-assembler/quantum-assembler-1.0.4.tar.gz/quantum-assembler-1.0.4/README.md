

# Configuration

## Excluding specific files

Add the filepath, relative to the project root directory, to
`.quantumignore`.

## Secrets management

A secret may either be an actual value or a placeholder.

### `qsa secret allow <vault> <keyid>`

Example:

`qsa secret allow staging BA38C91A6C74F11759A9DAF75430AD5398E322B9`

### `ApplicationSecretKey`

A secret key used by the application. The default implementation is
an AES256-compatible key, but specific implementations may deviate.
The secret key is commonly used for cookie-signing, JWT generation,
etc.


## Kubernetes

### `qsa k8s check`

Invoke `kubectl` to check if the cluster has all configurations
and secrets required to run the application, as determined from
the `Quantumfile`.
