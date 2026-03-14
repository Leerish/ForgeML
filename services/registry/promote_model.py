from services.registry.model_registry import (
    register_model,
    get_production_model,
    read_registry,
)


def promote_if_better(
    model_name,
    dataset_version,
    accuracy,
):

    prod = get_production_model(model_name)

    # First model ever
    if prod is None:

        register_model({
            "model_name": model_name,
            "version": "v1",
            "dataset_version": dataset_version,
            "accuracy": accuracy,
            "stage": "production"
        })

        return "promoted_first_model"

    # Better model
    if accuracy > prod["accuracy"]:

        new_version = f"v{int(prod['version'][1:]) + 1}"

        # Archive previous production model
        register_model({
            "model_name": prod["model_name"],
            "version": prod["version"],
            "dataset_version": prod["dataset_version"],
            "accuracy": prod["accuracy"],
            "stage": "archived"
        })

        # Promote new model
        register_model({
            "model_name": model_name,
            "version": new_version,
            "dataset_version": dataset_version,
            "accuracy": accuracy,
            "stage": "production"
        })

        return "promoted"

    return "rejected"