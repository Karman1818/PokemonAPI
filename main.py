from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
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






