# Receitas Backend

## Users

### Path: "/users/login" - POST
#### (autenticação não necessária)


#### POST:

Login de usuário padrão que retorna um token.

```json
{
    "username": "Example",
    "password": "password_example"
}

```
<hr>

### Path: "/users/" - GET, POST
#### (autenticação não necessária)

#### GET:

Retorna lista de usuários. Permite pesquisa através de query_params.

```json

```

#### POST:

Cria um novo usuário. Por padrão, ele estará desativado e será necessário utilizar um token enviado para o email informado aqui.

```json
{
    "username": "Example",
    "password": "example_password",
    "email": "example@gmail.com"
}

```

<hr>

### Path: "/users/<int:pk>" - GET
#### (autenticação não necessária)

#### GET:

Retorna as informações de um usuário em específico.

```json

```
<hr>

### Path: "/users/self" - GET, PUT, DELETE
#### (autenticação necessária)

#### GET:

Retorna as informações do usuário.

```json

```
<hr>

#### PUT:

Atualiza interamente ou parcialmente o usuário. Para alterar as informações, é necessário enviar suas credenciais junto aos campos.

```json
{
    "authorization": {
       "username": "Example",
       "password": "Example_password"
    },
    "new_data": {
       "username": "new_username"
    }
}
```

#### DELETE:

Deleta o usuário. Também requer o envio das credenciais.

```json
{
    "authorization": {
       "username": "Example",
       "password": "Example_password"
    }
}
```
<hr>

### Path: "/users/active-account" - POST
#### (autenticação não necessária)

#### POST:

Ativa a conta através do token enviado por email.

```json
{
    "activation_token": "HSHDUJE89D"
}
```
