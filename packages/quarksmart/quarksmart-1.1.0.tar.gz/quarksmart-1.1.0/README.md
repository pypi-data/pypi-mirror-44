# Quark Smart

O **quarksmart** é uma biblioteca Python que permite a integração entre ferramentas de *Data Science* com os dados armazenados no sistema [QuarkSmart](https://quarkbi.esig.com.br).

Com apenas um comando é possível carregar seus dados para um formato que permite o tratamento de forma fácil e ágil.
O quarksmart foi pensado para ser utilizado com outras bibliotecas de *Data Science*, como o ``pandas`` e o ``numpy``, mas nada você pode utiliza-la como preferir.

### Installing

A instalação da biblioteca é bem simples e pode ser realizada facilmente por meio do gerenciador de pacotes do python (pip).

Para instalar, abrir o terminal e rodar o comando abaixo do ``pip``: ::

    $ pip install quarksmart

Para verificar se a instalação aconteceu corretamente, basta importar o pacote e verificar a versão.

```python

   >>> import quarksmart
   >>> quarksmart.__version__
   '1.0.0'
```

## Built Dist

Para construir uma versão da biblioteca é preciso instalar a lib sdist:

    $ pip install sdist

Depois é só entrar na pasta do projeto e rodar o comando:

    $ python setup.py sdist


## Subindo para o PyPi

Para subir para o Pypi é preciso instalar outra biblioteca, o twine:

    $ pip install twice

Em seguida, entramos na pasta do projeto e rodamos o comando que vai subir para o ambiente de [testes](https://test.pypi.org/project/quarksmart/):

    $ twine upload dist/* --repository-url https://test.pypi.org/legacy/

Para subir para o ambiente de [produção](https://test.pypi.org/project/quarksmart/), devemos rodar:

    $ twine upload dist/*

## Authors

* **Rafael Dantas** - *Initial work* - [GitLab](https://git.esig.com.br/rafael.dantas)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc
