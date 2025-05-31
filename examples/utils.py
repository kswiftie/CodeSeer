import os, random, pathlib

DATASET = pathlib.Path(__file__).parent.parent / "dataset"


def read_random_task(dataset_root):
    tasks = [
        d
        for d in os.listdir(dataset_root)
        if os.path.isdir(os.path.join(dataset_root, d))
    ]

    chosen_task = random.choice(tasks)
    chosen_task_path = os.path.join(dataset_root, chosen_task)

    subfolders = ["original", "plagiarized", "non-plagiarized"]
    result = {"task": chosen_task, "files": []}

    for subfolder in subfolders:
        subfolder_path = os.path.join(chosen_task_path, subfolder)
        if os.path.isdir(subfolder_path):
            for filename in os.listdir(subfolder_path):
                file_path = os.path.join(subfolder_path, filename)
                if os.path.isfile(file_path):
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                    result["files"].append(
                        {
                            "source": subfolder,
                            "filename": filename,
                            "full_path": file_path,
                            "content": content,
                        }
                    )

    return result


def create_inputs():
    inp = []
    task_data = read_random_task(DATASET)
    for file in task_data["files"]:
        if file["source"] == "non-plagiarized":
            inp.append(
                (file["content"], file["source"] + "_" + file["filename"].strip(".py"))
            )
        else:
            inp.append((file["content"], file["source"]))
    return task_data["task"], inp
