def test_project_tree(cookies):
    result = cookies.bake(
        extra_context={
            'project_slug': 'pyconus2023',
            'production_environment': 'no'
        }
    )
    assert result.exit_code == 0
    assert result.exception is None

    assert result.project.basename == 'pyconus2023'
    assert result.project.isdir()

    generated_files = [
        'events/get_balance.json',
        'events/post_payment.json',
        'src/get_balance/app.py',
        'src/get_balance/requirements.txt',
        'src/post_payment/app.py',
        'src/post_payment/requirements.txt',
        'Makefile',
        'Pipfile',
        'README.md',
        'template.yaml'
    ]
    
    for file in generated_files:
        assert result.project.join(file).isfile()

def test_makefile(cookies):
    result = cookies.bake(
        extra_context={
            'aws_region': 'us-west-2',
            'aws_iam_profile': 'my-test-profile'
        }
    )
    app_file = result.project.join('Makefile')
    lines = app_file.readlines()
    assert "sam build --use-container --region us-west-2 --profile my-test-profile" in ''.join(lines)
    assert "sam deploy --guided --region us-west-2 --profile my-test-profile" in ''.join(lines)
    assert "sam deploy --region us-west-2 --profile my-test-profile" in ''.join(lines)


def test_get_balance_content_non_prod(cookies):
    result = cookies.bake(
        extra_context={
            'project_slug': 'pyconus2023',
            'production_environment': 'no'
        }
    )
    app_file = result.project.join('src/get_balance/app.py')
    lines = app_file.readlines()
    assert "from aws_lambda_powertools import Logger, Tracer" in ''.join(lines)
    assert "correlation_id_path=correlation_paths.API_GATEWAY_REST,\n    log_event=True" in ''.join(lines)


def test_get_balance_content_prod(cookies):
    result = cookies.bake(
        extra_context={
            'project_slug': 'pyconus2023',
            'production_environment': 'yes'
        }
    )
    app_file = result.project.join('src/get_balance/app.py')
    lines = app_file.readlines()
    # log_event=True should not be enabled in a production environment
    assert "from aws_lambda_powertools import Logger, Tracer" in ''.join(lines)
    assert "log_event=True" not in ''.join(lines)

def test_post_payment_content_non_prod(cookies):
    result = cookies.bake(
        extra_context={
            'project_slug': 'pyconus2023',
            'production_environment': 'no'
        }
    )
    app_file = result.project.join('src/post_payment/app.py')
    lines = app_file.readlines()
    assert "from aws_lambda_powertools import Logger, Tracer" in ''.join(lines)
    assert "correlation_id_path=correlation_paths.API_GATEWAY_REST,\n    log_event=True" in ''.join(lines)


def test_get_balance_content_prod(cookies):
    result = cookies.bake(
        extra_context={
            'project_slug': 'pyconus2023',
            'production_environment': 'yes'
        }
    )
    app_file = result.project.join('src/post_payment/app.py')
    lines = app_file.readlines()
    # log_event=True should not be enabled in a production environment
    assert "from aws_lambda_powertools import Logger, Tracer" in ''.join(lines)
    assert "log_event=True" not in ''.join(lines)

def test_prod_deployment_preference_in_sam_template(cookies):
    result = cookies.bake(
        extra_context={
            'project_slug': 'pyconus2023',
            'production_environment': 'yes',
            'deployment_preference': 'Linear10PercentEvery10Minutes'
        }
    )
    template_file = result.project.join('template.yaml')
    lines = template_file.readlines()
    assert "Linear10PercentEvery10Minutes" in ''.join(lines)
