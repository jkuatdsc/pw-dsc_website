from flask import make_response, jsonify
from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    jwt_refresh_token_required, get_jwt_identity
)    
from accounts.models import User
from DSC_jkuat.models import Article

parser = reqparse.RequestParser()

parser.add_argument(
    'content',
    required = True,
    help = 'Bad request: {error_msg}'
)
class CreateArticle(Resource):

    @jwt_refresh_token_required
    def post(self):
        article_parser = parser.copy()
        article_parser.add_argument(
            'title',
            required = True,
            help = 'Bad request: {error_msg}'  
        )
        article_parser.add_argument(
            'description',
            required = True,
            help = 'Bad request: {error_msg}'
        )
        data = article_parser.parse_args()
        current_user = get_jwt_identity()
        user = User.objects(username=current_user['username']).first() 
        if not user:
            return make_response(jsonify(
                msg='User %s does not exist' % (data['username'])
            ), 400)

        new_article = Article()
        new_article.title = data['title']
        new_article.description = data['description']
        new_article.author = user
        new_article.content = data['content']
        new_article.save()

        return make_response(jsonify(
            msg='article has been successfully created',
            article = new_article
        ), 201)

class GetArticle(Resource):
    def get(self, article_id):
        article = Article.objects(pk=article_id).first()
        if not article:
            return make_response(jsonify(
                msg='That article does not exist'
            ), 400)
        return make_response(jsonify(
            article = article
        ), 200)
        
class GetAllArticles(Resource):
    def get(self):
        articles = Article.objects()
        return make_response(jsonify(
            articles = articles
        ), 200)
