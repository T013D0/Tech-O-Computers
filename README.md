<a name="readme-top"></a>

<div align="center">
<a href="https://github.com/T013D0/Tech-O-Computers">
  <img width="300px" style="filter: drop-shadow(2px 2px 5px black)" src="https://i.imgur.com/52xkYdd.png" alt="Logo" width="800" />
</a>

## Proyecto Tech O Computers

Tech o Computers es una empresa ficticia diseñada para el proyecto de desarrollo de aplicaciones web

</div>

<details>
<summary>Tabla de contenidos</summary>

- [📱 Características principales](#características-principales)
  - [📸 Capturas de pantalla de Tech O Computers](#capturas-de-pantalla-de-la-web)
- [🏁 Para empezar](#para-empezar)
  - [📄 Prerequisitos](#prerequisitos)
  - [🖥️ Instalación](#instalación)
- [⚙️ Apis](#apis)
- [🛠️ Stack](#️stack)

</details>

## Características principales

- **Catálogo de Productos**: Explora una amplia gama de computadoras, periféricos y accesorios.
- **Compra en Línea**: Compra tus productos favoritos directamente desde nuestra página web.
- **Administración de Compras y Productos**: Gestiona tus compras, revisa el estado de tus pedidos y administra tu lista de productos fácilmente.


### Capturas de pantalla de la web
![Captura de pantalla en ordenador](https://i.imgur.com/n13j4ih.png)

<p align="right">(<a href="#readme-top">volver arriba</a>)</p>

## Para empezar

### Prerequisitos

- Python - ver [documentación oficial](https://docs.python.org/3/)

### Instalación

1. Clona el repositorio

    ```sh
    git clone https://github.com/T013D0/Tech-O-Computers.git
    ```

2. Instala los modulos

    ```sh
    pip install -r .\requirements.txt
    ```

3. Migra la base de datos

    ```sh
    python manage.py makemigrations
    python manage.py migrate
    ```

4. Ejecuta el proyecto

    ```sh
    python manage.py runserver
    ```

<p align="right">(<a href="#readme-top">volver arriba</a>)</p>

## Apis

- [Transbank API](https://www.transbankdevelopers.cl/referencia/webpay)
  - 
  ```@ensure_csrf_cookie
    @csrf_exempt
    def webpay_plus_create(request):
      data = json.loads(request.body)
      amount = data.get('amount')
      buy_order = str(random.randrange(1000000, 99999999))
      session_id = str(random.randrange(1000000, 99999999))
      return_url = request.build_absolute_uri(location='commitpay/')

      tx = Transaction(WebpayOptions(IntegrationCommerceCodes.WEBPAY_PLUS, IntegrationApiKeys.WEBPAY))
      response = tx.create(buy_order, session_id, amount, return_url)
      return JsonResponse({'url': response['url'], 'token': response['token']}) 
  ```
  [Tech-O-Computers/store/views.py](https://github.com/T013D0/Tech-O-Computers/blob/main/store/views.py#L188)

- [BigData Cloud API](https://www.bigdatacloud.com)
  - 
  ```
    const url =
    "https://api.bigdatacloud.net/data/reverse-geocode-client?latitude=XXXXXXXXXXXX&longitude=XXXXXXXXXXXX&localityLanguage=es";

  $.get(url, function (data) {
    const region = data.principalSubdivision;
    const city = data.locality;

    $("#state").val(region);
    $("#city").val(city);
    $(".input-disabled").prop("disabled", false);
    $("#shippingForm").show();
    $(".shipping-loader-container").remove();
    initMap({ latitude: data.latitude, longitude: data.longitude });
  });
  ```
  [Tech-O-Computers/static/js/shipping.js](https://github.com/T013D0/Tech-O-Computers/blob/main/static/js/shipping.js)

<p align="right">(<a href="#readme-top">volver arriba</a>)</p>

## Datos Compra

- Tarjeta Debito
  - 4051 8856 0044 6623
    CVV: 123 EXP: 12/28

- Usuario Transbank
  - Rut: 11.111.111-1
  - Contraseña: 123

<p align="right">(<a href="#readme-top">volver arriba</a>)</p>

## Stack

- [![Django][django-badge]][django-url] - The web framework.
- [![Bootstrap][bootstrap-badge]][bootstrap-url] - A CSS framework for responsive building custom designs.

<p align="right">(<a href="#readme-top">volver arriba</a>)</p>

[django-url]: https://www.djangoproject.com
[bootstrap-url]: https://getbootstrap.com
[django-badge]: https://img.shields.io/badge/Django-fff?style=for-the-badge&logo=django&logoColor=white&color=0C4B33
[bootstrap-badge]: https://img.shields.io/badge/bootstrap-007ACC?style=for-the-badge&logo=bootstrap&logoColor=white&color=5468ff
[contributors-shield]: https://img.shields.io/github/contributors/T013D0/Tech-O-Computers.svg?style=for-the-badge
[contributors-url]: https://github.com/T013D0/Tech-O-Computers/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/T013D0/Tech-O-Computers.svg?style=for-the-badge
[forks-url]: https://github.com/T013D0/Tech-O-Computers/network/members
[stars-shield]: https://img.shields.io/github/stars/T013D0/Tech-O-Computers.svg?style=for-the-badge
[stars-url]: https://github.com/T013D0/Tech-O-Computers/stargazers
[issues-shield]: https://img.shields.io/github/issues/T013D0/Tech-O-Computers.svg?style=for-the-badge
[issues-url]: https://github.com/T013D0/Tech-O-Computers/issues

