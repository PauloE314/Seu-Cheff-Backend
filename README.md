# Seu chef

<p align="center">
  <img src="https://i.ibb.co/N7RjwTk/headerseuchef.png" style="width: 100%; max-width: 600px">
</p><br>

**Seu Chef** é uma aplicação mobile com sistema backend dedicado que visa a criação e descobrimento de receitas. Com ele é possível guardar suas receitas em um local seguro (bem melhor que a forma tradicional em caderninhos) e ainda ver as receitas que outros usuários postaram.

O presente repositório é a implementação do sistema backend dedicado ao APP. Esse sistema foi construído seguindo o padrão RESTful.

## **Recursos**

- Cadastro, login e manutenção de conta de usuário com imagem
- Lista de receitas favoritas para cada usuário
- Criação, manutenção e listagem de receitas

## **Principais tecnologias**

- Python v3.8
- Django v3.0.7
- Django-rest-framework v3.11.0

## **Funcionamento**

A API das receitas é dividida nas seguintes seções:

- [Users](./docs/USERS.md)
- [Receitas](./docs/RECIPES.md)
