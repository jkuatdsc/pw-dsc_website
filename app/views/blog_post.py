from flask_restful import Resource, reqparse
from app.models.posts import BlogPost

class BlogPostView(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('title', type=str, required=True,
                        help='This field cannot be left blank')
    parser.add_argument('content', type=str, required=True,
                        help='This field cannot be left blank')

    def post(self):
        ''' Add new blog post '''
        apartment_request_data = BlogPostView.parser.parse_args()

        title = apartment_request_data['title']
        content = apartment_request_data['content']
        

        new_blog = BlogPost(title, content)
        new_blog.save()

        return {
            "Message":"Apartment created successfully"
        }, 201

