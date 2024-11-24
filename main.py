from fastapi import FastAPI, HTTPException
from pydantic import BaseModel,Field
from typing import List, Optional
from uuid import UUID,uuid4

app = FastAPI()


class Pokemon(BaseModel):
    id: Optional[UUID] = None
    name: str
    type: str
    level: int
    hp: int
    attack: int


pokemons = []


@app.post("/pokemons/",response_model=Pokemon)
def create_pokemon(pokemon: Pokemon):
    pokemon.id = uuid4()
    pokemons.append(pokemon)
    return pokemon


@app.get("/pokemons/", response_model=List[Pokemon])
def get_all_pokemons():
    return pokemons


@app.get("/pokemons/{pokemon_id}" , response_model=Pokemon)
def get_pokemon(pokemon_id: UUID):
    for pokemon in pokemons:
        if pokemon.id == pokemon_id:
            return pokemon
    raise HTTPException(status_code=404, detail="Pokemon not found")


@app.put("/pokemons/{pokemon_id}",response_model=Pokemon)
def update_pokemon(pokemon_id: UUID, pokemon_update: Pokemon):
    for idx, pokemon in enumerate(pokemons):
        if pokemon.id == pokemon_id:
            updated_pokemon = pokemon.copy(update=pokemon_update.dict(exclude_unset=True))
            pokemons[idx] = updated_pokemon
            return updated_pokemon
    raise HTTPException(status_code=404, detail="Pokemon not found")


@app.delete("/pokemons/{pokemon_id}",response_model=Pokemon)
def delete_pokemon(pokemon_id: UUID):
    for idx, pokemon in enumerate(pokemons):
        if pokemon.id == pokemon_id:
            return pokemons.pop(idx)
    raise HTTPException(status_code=404, detail="Pokemon not found")


class Trainer(BaseModel):
    id: Optional[UUID] = None
    firstName: str
    lastName: str
    age: Optional[int]
    gender: Optional[str]
    pokemonTeam: List[Pokemon] = Field(default_factory=list)


trainers = []


@app.post("/trainers/",response_model=Trainer)
def create_trainer(trainer: Trainer):
    if len(trainer.pokemonTeam) > 6:
        raise HTTPException(
            status_code=400, detail="A trainer can have only up to 6 Pokémon in their team."
        )
    trainer.id = uuid4()
    trainers.append(trainer)
    return trainer


@app.get("/trainers/", response_model=List[Trainer])
def get_all_trainers():
    return trainers


@app.get("/trainers/{trainer_id}", response_model=Trainer)
def get_trainer(trainer_id: UUID):
    for trainer in trainers:
        if trainer.id == trainer_id:
            return trainer
    raise HTTPException(status_code=404, detail="Trainer not found")


@app.post("/trainers/{trainer_id}/add_pokemon/{pokemon_id}", response_model=Trainer)
def add_pokemon_to_trainer(trainer_id: UUID, pokemon_id: UUID):
    for trainer in trainers:
        if trainer.id == trainer_id:
            if len(trainer.pokemonTeam) >= 6:
                raise HTTPException(status_code=400, detail="A trainer can have only 6 Pokémon in their team")
            for pokemon in pokemons:
                if pokemon.id == pokemon_id:
                    if any(pokemon.id == p.id for p in trainer.pokemonTeam):
                        raise HTTPException(status_code=400, detail="A trainer already has this Pokémon")
                    trainer.pokemonTeam.append(pokemon)
                    return trainer
            raise HTTPException(status_code=404, detail="Pokémon not found")
    raise HTTPException(status_code=404, detail="Trainer not found")


@app.delete("/trainers/{trainer_id}/remove_pokemon/{pokemon_id}", response_model=Trainer)
def delete_pokemon_from_trainer(trainer_id: UUID, pokemon_id: UUID):
    for trainer in trainers:
        if trainer.id == trainer_id:
            for idx,pokemon in enumerate(trainer.pokemonTeam):
                if pokemon.id == pokemon_id:
                    trainer.pokemonTeam.pop(idx)
                    return trainer
            raise HTTPException(status_code=404, detail="Pokémon not found")
    raise HTTPException(status_code=404, detail="Trainer not found")







