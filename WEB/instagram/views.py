from django.shortcuts import render
from django.http import HttpResponse
import requests
from django.views import View
from django.http import JsonResponse





class RegisterView(View):
    def get(self, request):
        return render(request, 'auth/register.html')


    def post(self, request):
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 == password2:

            api_url = 'http://127.0.0.1:8000/users/register/'

            data = {
                "username": username,
                "email": email,
                "password": password1
            }

            response = requests.post(api_url, json=data)

            if response.status_code == 200:
                return JsonResponse({'message': 'User registered successfully!', 'data': response.json()})
            else:
                return JsonResponse({'error': 'Failed to register user', 'details': response.json()},
                                    status=response.status_code)

        return JsonResponse({'error': 'Username and password are incorrect!'}, status=400)



class LoginView(View):
    def get(self, request):
        return render(request, 'auth/login.html')

    def post(self, request):
        username_or_email = request.POST.get('username_or_email')
        password = request.POST.get('password')

        api_url = 'http://127.0.0.1:8000/users/login/'

        data = {
            "username_or_email": username_or_email,
            "password": password
        }

        response = requests.post(api_url, json=data)
        if response.status_code == 200:
            return JsonResponse({'message': 'User logged in!', 'data': response.json()})

        else:
            return JsonResponse({'error': 'Failed to login user', 'details': response.json()},
                                status=response.status_code)



class HomeView(View):
    def get(self, request, *args, **kwargs):
        page = requests.get("http://127.0.0.1:8000/users/?size=2").json()['page']
        pages = requests.get("http://127.0.0.1:8000/users/?size=2").json()["pages"]

        if page is not None:
            if int(page) <= int(pages):
                data = requests.get("http://127.0.0.1:8000/users/?size=2").json()["items"]
                return render(request, "home.html",
                              context={"users": data, "pages": pages, "page": page, "next": int(page) + 1,
                                       "previous": int(page) - 1})

            data = requests.get(f"http://127.0.0.1:8000/users/?page={page}&size=2").json()["items"]
            return render(request, "home.html",
                          context={"users": data, "pages": pages, "page": page, "next": int(page) + 1,
                                   "previous": int(page) - 1})

        return render(request, "home.html", context={"message": "Not found"})




class PostView(View):
    def get(self, request, *args, **kwargs):
        page = requests.get("http://127.0.0.1:8000/posts/?size=1").json()['page']
        pages = requests.get("http://127.0.0.1:8000/posts/?size=1").json()["pages"]

        if page is not None:
            if int(page) <= int(pages):
                data = requests.get(f"http://127.0.0.1:8000/posts/?size=1").json()["items"]
                return render(request, "post.html",
                              context={"posts": data, "pages": pages, "page": 1, "next": 2, "previous": 0})

            data = requests.get(f"http://127.0.0.1:8000/posts/?page={page}&size=1").json()["items"]
            return render(request, "post.html",
                          context={"posts": data, "pages": pages, "page": page, "next": int(page) + 1,
                                   "previous": int(page) - 1})

        return render(request, "post.html", context={"message": "Not found"})



class CommentsView(View):
    def get(self, request, *args, **kwargs):
        page = requests.get(f"http://127.0.0.1:8000/comments/?size=2").json()['page']
        pages = requests.get(f"http://127.0.0.1:8000/comments/?size=2").json()["pages"]

        if page is not None:
            if int(page) <= int(pages):
                data = requests.get(f"http://127.0.0.1:8000/comments/?size=2").json()["items"]
                return render(request, "comment.html",
                              context={"comments": data, "pages": pages, "page": 1, "next": 2, "previous": 0})

            data = requests.get(f"http://127.0.0.1:8000/comments/?page={page}&size=2").json()["items"]
            return render(request, "comment.html",
                          context={"comments": data, "pages": pages, "page": page, "next": int(page) + 1,
                                   "previous": int(page) - 1})

        return render(request, "comment.html", context={"message": "Not found"})






# class HomeView(View):
#     def get(self, request, *args, **kwargs):
#         page = request.GET.get('page')
#         pages = requests.get("http://127.0.0.1:8000/users/?size=4").json()["pages"]
#
#         if int(page) <= int(pages):
#
#             if page is None:
#                 data = requests.get(f"http://127.0.0.1:8000/users/?size=4").json()["items"]
#                 return render(request, "home.html",
#                               context={"users": data, "pages": pages, "page": 1, "next": 2, "previous": 0})
#
#             data = requests.get(f"http://127.0.0.1:8000/users/?page={page}&size=4").json()["items"]
#             return render(request, "home.html",
#                           context={"users": data, "pages": pages, "page": page, "next": int(page) + 1,
#                                    "previous": int(page) - 1})
#
#         return render(request, "home.html", context={"message": "Not found"})
#
#
# class PostsView(View):
#     def get(self, request, *args, **kwargs):
#         page = request.GET.get('page')
#         pages = requests.get(f"http://127.0.0.1:8000/posts/?size=3").json()["pages"]
#
#         if int(page) <= int(pages):
#
#             if page is None:
#                 data = requests.get(f"http://127.0.0.1:8000/posts/?size=4").json()["items"]
#                 return render(request, "posts.html",
#                               context={"posts": data, "pages": pages, "page": 1, "next": 2, "previous": 0})
#
#             data = requests.get(f"http://127.0.0.1:8000/posts/?page={page}&size=4").json()["items"]
#             return render(request, "posts.html",
#                           context={"posts": data, "pages": pages, "page": page, "next": int(page) + 1,
#                                    "previous": int(page) - 1})
#
#         return render(request, "posts.html", context={"message": "Not found"})
#
#
# class CommentsView(View):
#     def get(self, request, *args, **kwargs):
#         page = request.GET.get('page')
#         pages = requests.get(f"http://127.0.0.1:8000/comments/?size=3").json()["pages"]
#
#         if int(page) <= int(pages):
#
#             if page is None:
#                 data = requests.get(f"http://127.0.0.1:8000/comments/?size=4").json()["items"]
#                 return render(request, "comments.html",
#                               context={"comments": data, "pages": pages, "page": 1, "next": 2, "previous": 0})
#
#             data = requests.get(f"http://127.0.0.1:8000/comments/?page={page}&size=4").json()["items"]
#             return render(request, "comments.html",
#                           context={"comments": data, "pages": pages, "page": page, "next": int(page) + 1,
#                                    "previous": int(page) - 1})
#
#         return render(request, "comments.html", context={"message": "Not found"})
#
#
#
#
# class FollowersView(View):
#     def get(self, request, *args, **kwargs):
#         page = request.GET.get('page')
#         pages = requests.get(f"http://127.0.0.1:8000/followers/?size=3").json()["pages"]
#
#         if int(page) <= int(pages):
#
#             if page is None:
#                 data = requests.get(f"http://127.0.0.1:8000/folowers/?size=4").json()["items"]
#                 return render(request, "followers.html",
#                               context={"followers": data, "pages": pages, "page": 1, "next": 2, "previous": 0})
#
#             data = requests.get(f"http://127.0.0.1:8000/followers/?page={page}&size=4").json()["items"]
#             return render(request, "followers.html",
#                           context={"followers": data, "pages": pages, "page": page, "next": int(page) + 1,
#                                    "previous": int(page) - 1})
#
#         return render(request, "followers.html", context={"message": "Not found"})
#
#
#
# class LikesView(View):
#     def get(self, request, *args, **kwargs):
#         page = request.GET.get('page')
#         pages = requests.get(f"http://127.0.0.1:8000/likes/?size=3").json()["pages"]
#
#         if int(page) <= int(pages):
#
#             if page is None:
#                 data = requests.get(f"http://127.0.0.1:8000/likes/?size=4").json()["items"]
#                 return render(request, "likes.html",
#                               context={"likes": data, "pages": pages, "page": 1, "next": 2, "previous": 0})
#
#             data = requests.get(f"http://127.0.0.1:8000/posts/?page={page}&size=4").json()["items"]
#             return render(request, "likes.html",
#                           context={"likes": data, "pages": pages, "page": page, "next": int(page) + 1,
#                                    "previous": int(page) - 1})
#
#         return render(request, "likes.html", context={"message": "Not found"})