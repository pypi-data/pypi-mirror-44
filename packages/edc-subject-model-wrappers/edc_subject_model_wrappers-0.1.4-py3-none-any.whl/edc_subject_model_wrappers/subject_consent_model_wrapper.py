from edc_model_wrapper import ModelWrapper


class SubjectConsentModelWrapper(ModelWrapper):

    model = None  # e.g. myapp.subjectconsent
    next_url_name = "subject_dashboard_url"
    next_url_attrs = ["subject_identifier"]
    querystring_attrs = [
        "screening_identifier",
        "gender",
        "first_name",
        "initials",
        "modified",
    ]
