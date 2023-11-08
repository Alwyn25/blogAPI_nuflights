# blog/schema.py
import graphene
from graphene_django.types import DjangoObjectType
from .models import Author, Post, Comment

class AuthorType(DjangoObjectType):
    class Meta:
        model = Author

class PostType(DjangoObjectType):
    class Meta:
        model = Post

class CommentType(DjangoObjectType):
    class Meta:
        model = Comment

class CreatePost(graphene.Mutation):
    class Arguments:
        title = graphene.String()
        description = graphene.String()
        publish_date = graphene.Date()
        author = graphene.String()

    post = graphene.Field(PostType)

    def mutate(self, info, title, description, publish_date, author):
        author_instance, created = Author.objects.get_or_create(name=author)
        post = Post(title=title, description=description, publish_date=publish_date, author=author_instance)
        post.save()
        return CreatePost(post=post)

class Mutation(graphene.ObjectType):
    create_post = CreatePost.Field()

schema = graphene.Schema(mutation=Mutation)

class UpdatePost(graphene.Mutation):
    class Arguments:
        id = graphene.Int()
        title = graphene.String()
        description = graphene.String()
        publish_date = graphene.Date()
        author_id = graphene.Int()

    post = graphene.Field(PostType)

    def mutate(self, info, id, title, description, publish_date, author_id):
        post = Post.objects.get(pk=id)
        post.title = title
        post.description = description
        post.publish_date = publish_date
        post.author = Author.objects.get(pk=author_id)
        post.save()
        return UpdatePost(post=post)

class CreateComment(graphene.Mutation):
    class Arguments:
        post_id = graphene.Int()
        text = graphene.String()
        author = graphene.String()

    comment = graphene.Field(CommentType)

    def mutate(self, info, post_id, text, author):
        post = Post.objects.get(pk=post_id)
        comment = Comment(post=post, text=text, author=author)
        comment.save()
        return CreateComment(comment=comment)

class DeleteComment(graphene.Mutation):
    class Arguments:
        id = graphene.Int()

    success = graphene.Boolean()

    def mutate(self, info, id):
        comment = Comment.objects.get(pk=id)
        comment.delete()
        return DeleteComment(success=True)

class Query(graphene.ObjectType):
    posts = graphene.List(PostType)
    post = graphene.Field(PostType, id=graphene.Int())

    def resolve_posts(self, info):
        return Post.objects.all()

    def resolve_post(self, info, id):
        return Post.objects.get(pk=id)

class Mutation(graphene.ObjectType):
    create_post = CreatePost.Field()
    update_post = UpdatePost.Field()
    create_comment = CreateComment.Field()
    delete_comment = DeleteComment.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
