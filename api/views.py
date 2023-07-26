from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.utils import short_name_is_valid
from .models import User, Pet, Toy
from .serializers import (
    UserSerializer,
    PetSerializer,
    ToySerializer,
)
from rest_framework.views import APIView
from django.db.models import Count


class UserView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


def check_user_email(user_email):
    if not user_email:
        return Response(data={"message": ["user_email is missing"]})

    user = User.get_user_by_email(user_email)
    if not user:
        return Response(
            data={
                "message": [
                    "El correo proporcionado no está registrado, por favor, regístrate y vuelva a intentarlo!"
                ]
            }
        )
    return user


class PetView(APIView):
    def get(self, _, user_email):
        """
        Ver las mascotas de un solo usuario, por medio de su correo
        """
        user = check_user_email(user_email)
        if type(user) is not User:
            return user

        pets = Pet.get_pets_by_user(user)
        return Response(data=pets.values())

    def post(self, request, user_email):
        user = check_user_email(user_email)
        if type(user) is not User:
            return user

        data = request.data

        data["user"] = user.id
        serializer = PetSerializer(data=request.data)
        if serializer.is_valid():
            short_name = data["short_name"] if "short_name" in data else None
            if not short_name_is_valid(short_name):
                return Response(
                    data={
                        "short_name": [
                            "El campo short_name solo acepta una palabra como máximo."
                        ]
                    }
                )

            serializer.save()
            return Response(
                data={"message": ["Mascota creada Correctamente!"]}, status=201
            )
        return Response(serializer.errors)

    def put(self, request, user_email, pk):
        user = check_user_email(user_email)
        if type(user) is not User:
            return User
        pet = Pet.objects.filter(id=pk, user=user)
        if len(pet) == 0:
            return Response(data={"message": "No existe la Mascota"})
        pet = pet.first()

        data = request.data
        data["user"] = user.id
        data["short_name"] = pet.short_name
        serializer = PetSerializer(pet, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(data={"message": ["Mascota modificada correctamente!"]})
        return Response(serializer.errors)

    def delete(self, _, user_email, pk):
        user = check_user_email(user_email)
        if type(user) is not User:
            return User
        pet = Pet.objects.filter(id=pk, user=user)
        if len(pet) == 0:
            return Response(data={"message": "No existe la Mascota"})
        pet = pet.first()
        pet.delete()
        return Response(200)


def get_existing_pets(request_pets, all_pets):
    return all_pets.filter(short_name__in=request_pets)


class ToyView(APIView):
    def post(self, request, user_email):
        user = check_user_email(user_email)
        if type(user) is not User:
            return User

        all_pets = Pet.get_pets_by_user(user)

        data = request.data
        if type(data) is dict:
            data = [data]

        for toy in data:
            request_pets = toy["pets"]
            pets_filter = get_existing_pets(request_pets, all_pets)
            pets_with_less_than_3_toys = pets_filter.annotate(
                num_toys=Count("toys")
            ).filter(num_toys__lt=3)

            pets_that_already_hace_3_toys = len(pets_filter) - len(
                pets_with_less_than_3_toys
            )

            serializer = ToySerializer(data=toy)
            if serializer.is_valid():
                toy_instance = Toy.objects.create(
                    name=toy["name"],
                    price=toy["price"],
                    purchase_url=toy["purchase_url"],
                )
                toy_instance.pets.set(pets_with_less_than_3_toys)
                return Response(
                    data={
                        "message": [
                            "Se creó el nuevo juguete y se asignó a sus mascotas",
                            f"Se obviaron {pets_that_already_hace_3_toys} mascotas, por que ya cuentan con 3 juguetes!"
                            if pets_that_already_hace_3_toys > 0
                            else None,
                        ]
                    },
                    status=200,
                )

        return Response(data=serializer.errors)
