# Copyright (c) 2023, NVIDIA CORPORATION.  All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import time

import numpy as np
import tritonclient.grpc as triton_grpc
import tritonclient.utils
from PIL import Image


def main():
    grpc_client = triton_grpc.InferenceServerClient(url="localhost:8001", verbose=False)
    prompt = "A photo of a Shiba Inu dog with a backpack riding a bike. It is wearing sunglasses and a beach hat."
    control = Image.open("/data/control.png").convert("RGB")

    triton_input_grpc = [
        triton_grpc.InferInput("prompt", (1,), tritonclient.utils.np_to_triton_dtype(np.object_)),
        triton_grpc.InferInput(
            "control", (control.height, control.width, 3), tritonclient.utils.np_to_triton_dtype(np.uint8),
        ),
    ]

    triton_input_grpc[0].set_data_from_numpy(np.array(prompt, dtype=np.object_).reshape(1))
    triton_input_grpc[1].set_data_from_numpy(np.array(control))

    triton_output_grpc = triton_grpc.InferRequestedOutput("generated_image")
    t = time.perf_counter()
    request_grpc = grpc_client.infer(
        "controlnet", model_version="1", inputs=triton_input_grpc, outputs=[triton_output_grpc],
    )
    out = (request_grpc.as_numpy("generated_image") * 255).astype(np.uint8)
    print(f"Client request took: {time.perf_counter() - t:.2f}s")

    for i in range(out.shape[0]):
        Image.fromarray(out[i]).save(f"controlnet_output_{i}.jpg")


if __name__ == "__main__":
    main()
