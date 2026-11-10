import uuid
from typing import Optional
from pydantic import BaseModel, constr


class GenerationHistoryBase(BaseModel):
    id: Optional[uuid.UUID] = None
    prompt: Optional[str] = None
    inputs: Optional[dict] = None
    output: Optional[dict] = None
    is_deleted: Optional[bool] = False
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    user_id: Optional[str] = None

    class Config:
        orm_mode = True


class GenerationHistoryCreate(GenerationHistoryBase):
    pass


class GenerationHistoryUpdate(GenerationHistoryBase):
    pass


class GenerateImageInput(BaseModel):
    prompt: str = "A painting of a beautiful sunset"
    # count: int = 1
    # width: int = 1024
    # height: int = 1024
    # # refine: str = "expert_ensemble_refiner"
    # scheduler: constr(pattern='^(DDIM|DPMSolverMultistep|HeunDiscrete|KarrasDPM|K_EULER_ANCESTRAL|K_EULER|PNDM)$') = "DDIM"
    # guidance_scale: float = 7.5
    # high_noise_frac: float = 0.8
    # prompt_strength: float = 0.8
    # num_inference_steps: int = 50
