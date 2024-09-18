from boexplorer.transforms.utils import current_date_iso


def add_annotation(annotations, description, pointer):
    """Add commenting annotation to statement"""
    annotation = {'motivation': 'commenting',
                  'description': description,
                  'statementPointerTarget': pointer,
                  'creationDate': current_date_iso(),
                  'createdBy': {'name': 'Open Ownership',
                                'uri': "https://www.openownership.org"}}
    annotations.append(annotation)

def add_lei_annotation(annotations, lei, registration_status):
    """Annotation of status for all entity statements (not generated as a result
       of a reporting exception)"""
    add_annotation(annotations,
                   f"GLEIF data for this entity - LEI: {lei}; Registration Status: {registration_status}",
                   "/")
