from django.apps import apps
from django.shortcuts import render, redirect
from django.http import JsonResponse

from app.forms import AlgoRequestForm, DatabaseChoiceForm
from app.algos import run as run_algo

from app.databases import get_database_attributes, get_databases

from app.models import Node, Node2, Node3
from collections import Counter


# Function Tests
Node2.objects.all()
Node3.objects.all()
