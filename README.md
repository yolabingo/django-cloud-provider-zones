# Django Cloud Provider Regions

This [Django app](https://docs.djangoproject.com/en/5.0/ref/applications/) provides a static list of region and availability zones for AWS (Amazon Web Services) and GCP (Google Cloud Platform) cloud providers.

The purpose of this app is to provide Cloud Provider Region/AZ lists easily available to Django apps. It provides stable, shortened, versions of names for provisioning  naming conventions.

The Regions/AZ list is currrent as of March 2024.

## Features
- Simple access to cloud Region and AZs from other DJjango apps
- Provides shortened versions of Region and AZ names for use by provisioning tools
- DB primary key fields are stable, will not change as new Regions/AZs are added

## Installation

### Models

This app provides the following models:

- `CloudProvider`: Cloud provider names - currently `AWS` or `GCP` 
- `Region`: Cloud regions
- `AvailabilityZone`: Availability zones within a region

### API Endpoints

The following API endpoints are available:

- `GET /api/regions/`: Retrieve a list of all regions.
- `GET /api/regions/<region_id>/`: Retrieve details of a specific region.

### Sample Code

```python
# Example usage of the Django models and API
import requests

# Create a new region
new_region_data = {
    "name": "us-west1",
    "provider": "GCP"
}
response = requests.post("http://127.0.0.1:8000/api/regions/", json=new_region_data)
print(response.json())  # Newly created region data

# Retrieve all regions
regions_response = requests.get("http://127.0.0.1:8000/api/regions/")
print(regions_response.json())  # List of all regions
```

## Contributing

Contributions are welcome! Please feel free to open issues or submit pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Notes 

[GCP Python Quickstart](https://developers.google.com/docs/api/quickstart/python)


## Acknowledgments

- Thanks to the Django community and Django Software Foundation for Django
- Thanks to the maintainers of all dependencies on this project
- Thanks to Real Python for their [Installable Django App article](https://realpython.com/installable-django-app/)# django-cloud-provider-regions