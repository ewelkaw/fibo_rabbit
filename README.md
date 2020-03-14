## 1. Running app:

Using Docker in the main dir:

```
docker-compose up
```

**Or locally:**

Setup:
```
python3 -m venv venv
. venv/bin/activate
pip3 install -r requirements
```

API:
```source venv/bin/activate
export FLASK_ENV=development
export FLASK_APP=api.api
flask run --host=0.0.0.0
```

Generator:
```source venv/bin/activate
python3 generator/generator.py
```

Processor:
```source venv/bin/activate
python3 processor/processor.py
```

You need to have RabbitMQ running locally for that to work. 
Optionally, you can configure address to Rabbit using `RABBIT_HOST` env variable.

## 2. Requesting API:

**GET:**

`localhost:8000/api/fibo_sequence/<<your_number>>`

**POST:**

`localhost:8000/api/fibo_sequence`

body:
```
{
	"number": <<your_number>>
}
```

header:
```
Content-Type: application/json
Accept: application/json
```