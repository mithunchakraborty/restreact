from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Customer
from .serializers import *


@api_view(['GET', 'POST'])
def customers_list(request):
    """
    List customers, or create a new customer.
    """

    """
    If it is a GET request, the method paginates the data using Django 
    Paginator and returns the first page of data after serialization, 
    the number of clients available, the number of available pages, 
    and links to the previous and next pages. Paginator is a built-in 
    Django class for paginating a list of data and providing accessor 
    methods for elements on each page.
    
    If it is a POST request, the method serializes the received client 
    data and then calls the save () method using the serializer object. 
    It then returns a Response object that is an HttpResponse instance 
    with status code 201. Each view that is created is responsible for 
    returning an HttpResponse object. The save () method saves the 
    serialized data to the database.
    """
    if request.method == 'GET':
        data = []
        nextPage = 1
        previousPage = 1
        customers = Customer.objects.all()
        page = request.GET.get('page', 1)
        paginator = Paginator(customers, 10)

        try:
            data = paginator.page(page)
        except PageNotAnInteger:
            data = paginator.page(1)
        except EmptyPage:
            data = paginator.page(paginator.num_pages)

        serializer = CustomerSerializer(
            data,
            context={'request': request},
            many=True
        )

        if data.has_next():
            nextPage = data.next_page_number()

        if data.has_previous():
            previousPage = data.previous_page_number()

        return Response({
            'data': serializer.data,
            'count': paginator.count,
            'numpages': paginator.num_pages,
            'nextlink': '/api/customers/?page=' + str(nextPage),
            'prevlink': '/api/customers/?page=' + str(previousPage)
        })

    elif request.method == 'POST':
        serializer = CustomerSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['GET', 'PUT', 'DELETE'])
def customers_detail(request, pk):
    """
    Retrieve, update or delete a customer by id/pk.
    """
    try:
        customer = Customer.objects.get(pk=pk)
    except Customer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    """
    If it is a GET request, the client data is serialized and 
    sent using the Response object.

    If it is a PUT request, the method creates a serializer for the new 
    client data. It then calls the save () method of the created serializer 
    object. Finally, it dispatches a Response object with the updated client data.

    If it is a DELETE request, the method calls the delete () method of 
    the customer object to delete it, and then returns a Response object 
    containing no data.
    """
    if request.method == 'GET':
        serializer = CustomerSerializer(
            customer,
            context={'request': request}
        )

        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = CustomerSerializer(
            customer,
            data=request.data,
            context={'request': request}
        )

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)

        return Response(
            serializer.errors, 
            status=status.HTTP_400_BAD_REQUEST
        )

    elif request.method == 'DELETE':
        customer.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

