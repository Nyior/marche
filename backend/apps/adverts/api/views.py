from rest_framework.response import Response

from rest_framework import (generics, 
                            viewsets, 
                            mixins, 
                            filters)

from rest_framework.permissions import (IsAuthenticatedOrReadOnly, 
                                        IsAuthenticated)

from rest_framework.generics import get_object_or_404

from rest_framework.parsers import  (MultiPartParser, 
                                        FormParser, 
                                        FileUploadParser)

from rest_framework.decorators import api_view

from apps.adverts.api.permissions import *

from apps.adverts.models import Advert
from apps.users.models import CustomUser

from apps.adverts.api.serializers import *
from apps.users.api.serializers import CustomUserSerializer

from apps.core.utils import generate_unique_slug


@api_view(['GET'])
def general_search(request):
	"""
	This is used for general searches. it returns search results based on a user's input.
	The search result could either be a user,or an advert.
	"""
	query = request.GET.get("search", None)

	if query:
		adverts = Advert.objects.all()
		users = CustomUser.objects.all()
		serializer_context = {"request":request}

		adverts = adverts.filter(name__icontains=query)
		users = users.filter(username__icontains=query)
				
		return Response({
						"users": CustomUserSerializer(
                                                    users, 
                                                    many=True, 
                                                    context=serializer_context
                                                    ).data,
						"adverts": AdvertSerializer(
                                                    adverts, 
                                                    many=True, 
                                                    context=serializer_context
                                                    ).data
					    })

	return Response(
                {
                    'success': False,

                    'message': "You need to pass a query param"

                })


class AdvertViewSet(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    """ This generates crud views for adverts.
    """

    queryset = Advert.objects.all().order_by("-date_created")
    lookup_field = 'slug'
    serializer_class = AdvertSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsUserOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]

    def perform_update(self, serializer):
        cat = self.request.data["category"] 
        category = get_object_or_404(Category, name=cat)
        serializer.save(category=category)

    def perform_create(self, serializer):
        slug = generate_unique_slug(self.request.data["name"])
        cat = self.request.data["category"] 
        user = self.request.user
        category = get_object_or_404(Category, name=cat)
        serializer.save(slug=slug, user=user, category=category)


class CategoryListAPIView(generics.ListAPIView):
    """ This returns a list of product categories
    """
    serializer_class = AdvertSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        kwarg_slug = self.kwargs.get("category")
        return Advert.objects.filter(category__name=kwarg_slug).order_by("-date_created")


class SellerShopAPIView(generics.ListAPIView):
    """ This returns a list of adverts created by a user
    """

    serializer_class = AdvertSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        user_id = self.kwargs.get("user_id")
        user = get_object_or_404(CustomUser, id=user_id)
        return user.adverts.all().order_by("-date_created")