from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Book REST API",
      default_version='v1',
      description="""
      #### This REST API provides operations for managing users, profiles, books, literary genres, publishers and user reviews.

      ### Main Operations:
      
      ### Books:

      * #### Publish a book: Allows administrator users to publish a book.
      * #### List of books: A list of books.
      * #### Detail of books: Shows the details of a book.
      * #### Update a book: Allows administrator users to modify books.
      * #### Delete a book: Allows administrator users to delete books.

      ### Genders:

      * #### Add a gender: Allows the administrator users to create genres for the publication of books.
      * #### Detail a gender: Shows the details of a gender.
      * #### List of genders: A list of books.
      * #### Delete gender: Allows administrator users to delete genres.
      * #### Update gender: Allows administrator users to update the genres of the books.

      ### Publishers:
            
      * #### Create a publisher: Allows administrator users to create publishers for the publication of books.
      * #### Detail a publisher: It shows the details of the publisher and the books that belong to it.
      * #### Delete a publisher: Allows administrator users delete publishers.
      * #### Update a publisher: Allows administrator users to update publisher data.
      * #### List of Books from the publisher: A list of the publisher's books.

      ### Reviews:

      * #### Create a review: Allows users to create book reviews.
      * #### Delete a review: Allows users to delete their reviews.
      * #### Update a review: Allows users update their reviews.
      * #### List of reviews from specific book: A list of reviews of a specific book.
      * #### Detail a review: Allows the visualization of the reviews

      ### Profiles:

      * #### Create a profile: Allows the creation of profiles automatically at the time of user registration. 
      * #### Update a profile: Allows you to update your corresponding profiles.
      * #### Detail a profile: Allows viewing of profile data.
      """,
      contact=openapi.Contact(email="folco.carril@gmail.com"),
      license=openapi.License(name="MIT License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)