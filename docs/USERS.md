# Users

### **PATH:** ``` /users/login/ ``` - POST

#### POST: (Autenticação não necessária)

Essa URL serve para realizar o login (username e senha) dos usuários ativos (que o email já foi validado) retornando um token que será utilizado nas requisições HTTP.

```json
{
    "username": "Example",
    "password": "example_password"
}
```

<hr>

### **PATH:** ``` /users/ ``` - GET, POST

#### GET: (Autenticação não necessária)

Retorna a lista de usuários ativos. Aceita parâmetros de busca para filtrar os usuário:
- ```/users/?username=Example```

#### POST: (Autenticação não necessária)

Cria um novo usuário não ativo.
```json
{
    "username": "Example",
    "password": "example_password",
    "email": "example@gmail.com"
}
```
<hr>

### **PATH:** ``` /users/active-account/ ``` - POST

Ativa um usuário através do Token de ativação enviado para o seu email.

```json
{
    "activation-token": "ASNKMFJA"
}
```

<hr>

### **PATH:** ``` /users/<int:pk> ``` - GET

#### GET: (Autenticação não necessária)
Retorna um usuário detentor do id na URL. Também retorna a lista de receitas que esse usuário possui.

```json
{
    "id": 1,
    "username": "Example",
    "email": "example@agmail.com",
    "image": null, 
    "recipes": [
        {
            "id": 1,
            "favorites": 2,
            "created_at": "2020-05-12T09:25:48.832176-03:00",
            "last_update": "2020-05-12T10:01:53.514038-03:00",
            "title": "Feijoada 2",
            "image": null,
            "time": 20.0,
            "food_yield": 5,
            "ingredients": [
                "Feijão",
                "Linguiça",
                "literalmente qualquer coisa"
            ],
            "steps": [
                "Cozinha o feijão",
                "cabou"
            ],
            "additional_information": "É muito bom, namoral",
            "food_type": "Brasileira"
        }
    ]
}
```

<hr>

### **PATH:** ``` /users/self/ ``` - GET, PUT, DELETE

#### GET: (Autenticação necessária)

Retorna as informações do usuário logado. Suas receitas são pegas em outra URL especificada mais a frente

#### PUT: (Autenticação necessária)

Para atualizar as informações do usuário, é necessário enviar o as credenciais dele, para ter ceterza que é ele mesmo.
```json
{
    "authorization": {
        "username": "example",
        "password": "example_password"
    },
    "new_data": {
        "username": "new_username"
    }
}
```

#### DELETE: (Autenticação necessária)

Assim como no PUT, no delete é necessário enviar as credenciais.

<hr>

### **PATH:** ``` /users/self/image/ ``` - PUT, DELETE

#### PUT: (autenticação necessária)

Permite alterar a imagem de um usuário.

```javascript
const fd = new FormData();
const img = document.getElementById('image').files[0];

fd.append('image', img);

fetch('path/users/self/image/', {
    method: "PUT",
    ...
    body: fd
})
```

#### DELETE: (autenticação necessária)

Deleta a imagem do usuário

<hr>

### **PATH:** ``` /users/self/favorites/ ``` - GET

#### GET: (Autenticação necessária)

Retorna a lista de receitas favoritadas pelo usuário