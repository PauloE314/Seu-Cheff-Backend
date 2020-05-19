# Recipes

### **PATH:** ``` /recipes/ ``` - GET

#### GET: (Autenticação não necessária)

Retorna a lista de receitas. Aceita parâmetros para filtrar a pesquisa:
- ```/recipes/?name=Feijão```
- ```/recipes/?food_type=Brasileira```

<hr>

### **PATH:** ``` /recipes/self/ ``` - GET, POST

#### GET: (Autenticação necessária)

Retorna a lista de receitas que o usuário fez. Aceita parâmetros para filtrar a pesquisa:
- ```/recipes/?name=Feijão```
- ```/recipes/?food_type=Brasileira```

#### POST: (Autenticação necessária)

Cria uma nova receita com o usuário como autor.

```json
{
    "title": "New Food",
    "time": 30,
    "food_yield": 5,
    "ingredients": [
        "ingrediente_1",
        "ingrediente_2"
    ],
    "steps": [
        "lorem",
        "ipsum",
        "dolor",
        "amet"
    ],
    "additional_information": "Lorem upsum dolor amet",
    "food_type": "DOC",
}
```
<hr>

### **PATH:** ``` /recipes/self/<int:pk> ``` - GET, PUT, DELETE

#### GET: (autenticação necessária)

Retorna a receita especifica que o usuário fez.

#### PUT: (autenticação necessária)

Altera alguma informação da receita.

```json
{
    "food_yield": 20
}
```

#### DELETE: (autenticação necessária)

Para deletar a receita, é necessário enviar as credenciais do autor.
 ```json
{
    "authorization": {
        "username": "example",
        "password": "example_password"
    }
}
 ```
<hr>

### **PATH:** ``` /recipes/self/<int:pk>/image/ ``` - GET, PUT, DELETE

#### GET: (autenticação necessária)

Retorna alguma receita.

#### PUT: (autenticação necessária)

Permite alterar a imagem de uma receita.

```javascript
const fd = new FormData();
const img = document.getElementById('image').files[0];

fd.append('image', img);

fetch('path/recipes/self/1/image', {
    method: "PUT",
    ...
    body: fd
})
```

#### DELETE: (autenticação necessária)

Deleta a imagem de uma receita


<hr>


### **PATH:** ``` /recipes/self/favorites/<int:pk> ``` - POST

#### POST: (Autenticação necessária)

Favoria uma receita (do id na url), caso ela já esteja favoritada a receita será retirada da lista de favoritos