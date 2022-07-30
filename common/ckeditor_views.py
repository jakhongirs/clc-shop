from ckeditor_uploader.views import *  # noqa

HOST = getattr(settings, "HOST")


def get_files_browse_urls(user=None):
    """
    Recursively walks all dirs under upload dir and generates a list of
    thumbnail and full image URL's for each file found.
    """
    files = []
    for filename in get_image_files(user=user):
        src = utils.get_media_url(filename)
        if getattr(settings, "CKEDITOR_IMAGE_BACKEND", None):
            if is_valid_image_extension(src):
                thumb = utils.get_media_url(utils.get_thumb_filename(filename))
            else:
                thumb = utils.get_icon_filename(filename)
            visible_filename = os.path.split(filename)[1]
            if len(visible_filename) > 20:
                visible_filename = visible_filename[0:19] + "..."
        else:
            thumb = src
            visible_filename = os.path.split(filename)[1]
        files.append(
            {
                "thumb": "%s%s" % (HOST, thumb),
                "src": "%s%s" % (HOST, src),
                "is_image": is_valid_image_extension(src),
                "visible_filename": visible_filename,
            }
        )
    return files


class ImageUploadView(generic.View):
    http_method_names = ["post"]

    def post(self, request, **kwargs):
        """
        Uploads a file and send back its URL to CKEditor.
        """
        uploaded_file = request.FILES["upload"]

        backend = registry.get_backend()

        ck_func_num = request.GET.get("CKEditorFuncNum")
        if ck_func_num:
            ck_func_num = escape(ck_func_num)

        filewrapper = backend(storage, uploaded_file)
        allow_nonimages = getattr(settings, "CKEDITOR_ALLOW_NONIMAGE_FILES", True)
        # Throws an error when an non-image file are uploaded.
        if not filewrapper.is_image and not allow_nonimages:
            return HttpResponse(
                """
                <script type='text/javascript'>
                window.parent.CKEDITOR.tools.callFunction({0}, '', 'Invalid file type.');
                </script>""".format(
                    ck_func_num
                )
            )

        filepath = get_upload_filename(uploaded_file.name, request)

        saved_path = filewrapper.save_as(filepath)

        url = utils.get_media_url(saved_path)

        if ck_func_num:
            # Respond with Javascript sending ckeditor upload url.
            return HttpResponse(
                """
            <script type='text/javascript'>
                window.parent.CKEDITOR.tools.callFunction({0}, '{1}');
            </script>""".format(
                    ck_func_num, url
                )
            )
        else:
            _, filename = os.path.split(saved_path)
            retdata = {
                "url": "%s%s" % (HOST, url),
                "uploaded": "1",
                "fileName": filename,
            }
            return JsonResponse(retdata)


upload = csrf_exempt(ImageUploadView.as_view())


def browse(request):
    files = get_files_browse_urls(request.user)
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data.get("q", "").lower()
            files = list(
                filter(lambda d: query in d["visible_filename"].lower(), files)
            )
    else:
        form = SearchForm()

    show_dirs = getattr(settings, "CKEDITOR_BROWSE_SHOW_DIRS", False)
    dir_list = sorted(set(os.path.dirname(f["src"]) for f in files), reverse=True)

    # Ensures there are no objects created from Thumbs.db files - ran across
    # this problem while developing on Windows
    if os.name == "nt":
        files = [f for f in files if os.path.basename(f["src"]) != "Thumbs.db"]

    context = {"show_dirs": show_dirs, "dirs": dir_list, "files": files, "form": form}
    return render(request, "ckeditor/browse.html", context)
