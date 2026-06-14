from pydantic import BaseModel, Field
from typing import Union, Literal

class SwordSchema(BaseModel):
    asset_type: Literal["sword"] = "sword"
    blade_length: float = Field(default=90.0, ge=40.0, le=150.0, description="Blade length in centimeters")
    blade_width: float = Field(default=5.0, ge=2.0, le=15.0, description="Blade width in centimeters")
    grip_length: float = Field(default=15.0, ge=10.0, le=30.0, description="Grip length in centimeters")
    crossguard_type: Literal["simple", "curved", "none"] = Field(default="simple", description="Type of hilt crossguard")
    grip_material: Literal["leather", "wood", "metal"] = Field(default="leather", description="Grip material wrap")

class DaggerSchema(BaseModel):
    asset_type: Literal["dagger"] = "dagger"
    blade_length: float = Field(default=38.0, ge=20.0, le=70.0, description="Blade length in centimeters")
    blade_width: float = Field(default=3.8, ge=1.5, le=8.0, description="Blade width in centimeters")
    grip_length: float = Field(default=11.0, ge=7.0, le=18.0, description="Grip length in centimeters")
    crossguard_type: Literal["simple", "curved", "none"] = Field(default="simple", description="Type of hilt crossguard")
    grip_material: Literal["leather", "wood", "metal"] = Field(default="leather", description="Grip material wrap")

class HammerSchema(BaseModel):
    asset_type: Literal["hammer"] = "hammer"
    handle_length: float = Field(default=90.0, ge=45.0, le=150.0, description="Hammer handle length in centimeters")
    head_width: float = Field(default=24.0, ge=12.0, le=45.0, description="Hammer head width in centimeters")
    head_height: float = Field(default=14.0, ge=8.0, le=28.0, description="Hammer head height in centimeters")
    head_material: Literal["steel", "brass", "stone"] = Field(default="steel", description="Material of the hammer head")
    handle_material: Literal["wood", "metal"] = Field(default="wood", description="Material of the hammer handle")

class MaceSchema(BaseModel):
    asset_type: Literal["mace"] = "mace"
    shaft_length: float = Field(default=88.0, ge=45.0, le=140.0, description="Mace shaft length in centimeters")
    head_radius: float = Field(default=11.0, ge=5.0, le=20.0, description="Mace head radius in centimeters")
    flange_count: int = Field(default=6, ge=4, le=10, description="Number of flanges around the mace head")
    shaft_material: Literal["wood", "metal"] = Field(default="wood", description="Material of the mace shaft")
    head_material: Literal["iron", "steel", "brass"] = Field(default="iron", description="Material of the mace head")

class SpearSchema(BaseModel):
    asset_type: Literal["spear"] = "spear"
    shaft_length: float = Field(default=240.0, ge=120.0, le=360.0, description="Spear shaft length in centimeters")
    tip_length: float = Field(default=42.0, ge=15.0, le=80.0, description="Spear tip length in centimeters")
    shaft_material: Literal["wood", "metal"] = Field(default="wood", description="Material of the spear shaft")
    tip_material: Literal["steel", "iron", "brass"] = Field(default="steel", description="Material of the spear tip")

class HalberdSchema(BaseModel):
    asset_type: Literal["halberd"] = "halberd"
    shaft_length: float = Field(default=260.0, ge=150.0, le=420.0, description="Halberd shaft length in centimeters")
    blade_size: float = Field(default=48.0, ge=24.0, le=90.0, description="Main halberd blade size in centimeters")
    hook_size: float = Field(default=22.0, ge=10.0, le=40.0, description="Rear hook size in centimeters")
    shaft_material: Literal["wood", "metal"] = Field(default="wood", description="Material of the halberd shaft")
    head_material: Literal["steel", "iron", "brass"] = Field(default="steel", description="Material of the halberd head")

class StaffSchema(BaseModel):
    asset_type: Literal["staff"] = "staff"
    height: float = Field(default=190.0, ge=120.0, le=280.0, description="Staff height in centimeters")
    shaft_radius: float = Field(default=2.5, ge=1.0, le=6.0, description="Staff shaft radius in centimeters")
    material: Literal["wood", "darkwood", "bone"] = Field(default="wood", description="Material of the staff shaft")
    tip_style: Literal["plain", "ring", "carved"] = Field(default="plain", description="Style of the staff tip")

class BowSchema(BaseModel):
    asset_type: Literal["bow"] = "bow"
    height: float = Field(default=170.0, ge=90.0, le=240.0, description="Overall bow height in centimeters")
    width: float = Field(default=56.0, ge=25.0, le=110.0, description="Curved bow depth/width in centimeters")
    material: Literal["wood", "darkwood", "bone"] = Field(default="wood", description="Material of the bow limbs")
    bow_style: Literal["longbow", "recurve", "shortbow"] = Field(default="longbow", description="Bow silhouette style")

class CrossbowSchema(BaseModel):
    asset_type: Literal["crossbow"] = "crossbow"
    width: float = Field(default=82.0, ge=45.0, le=160.0, description="Crossbow limb span in centimeters")
    stock_length: float = Field(default=96.0, ge=45.0, le=160.0, description="Crossbow stock length in centimeters")
    material: Literal["wood", "darkwood", "steel"] = Field(default="wood", description="Primary crossbow stock material")
    has_bolt: bool = Field(default=True, description="Whether the crossbow includes a loaded bolt")

class ArrowSchema(BaseModel):
    asset_type: Literal["arrow"] = "arrow"
    length: float = Field(default=78.0, ge=35.0, le=120.0, description="Arrow length in centimeters")
    shaft_radius: float = Field(default=1.0, ge=0.3, le=2.5, description="Arrow shaft radius in centimeters")
    shaft_material: Literal["wood", "darkwood", "bone"] = Field(default="wood", description="Material of the arrow shaft")
    tip_material: Literal["steel", "brass", "obsidian"] = Field(default="steel", description="Material of the arrow tip")
    fletching_color: Literal["white", "red", "black", "green", "blue"] = Field(default="white", description="Primary fletching color")

class BoltSchema(BaseModel):
    asset_type: Literal["bolt"] = "bolt"
    length: float = Field(default=34.0, ge=18.0, le=70.0, description="Crossbow bolt length in centimeters")
    shaft_radius: float = Field(default=1.3, ge=0.4, le=3.0, description="Crossbow bolt shaft radius in centimeters")
    shaft_material: Literal["wood", "darkwood", "bone"] = Field(default="wood", description="Material of the bolt shaft")
    tip_material: Literal["steel", "brass", "obsidian"] = Field(default="steel", description="Material of the bolt tip")
    fletching_color: Literal["white", "red", "black", "green", "blue"] = Field(default="white", description="Primary bolt fletching color")

class MagicStaffSchema(BaseModel):
    asset_type: Literal["magic_staff"] = "magic_staff"
    height: float = Field(default=210.0, ge=140.0, le=320.0, description="Magic staff height in centimeters")
    shaft_material: Literal["wood", "darkwood", "obsidian"] = Field(default="darkwood", description="Material of the magic staff shaft")
    gem_color: Literal["blue", "green", "red", "purple"] = Field(default="blue", description="Primary magical gem color")
    head_style: Literal["orb", "crystal", "crescent"] = Field(default="orb", description="Style of the magical head ornament")

class WandSchema(BaseModel):
    asset_type: Literal["wand"] = "wand"
    length: float = Field(default=32.0, ge=18.0, le=55.0, description="Wand length in centimeters")
    shaft_material: Literal["wood", "bone", "obsidian"] = Field(default="wood", description="Material of the wand shaft")
    tip_style: Literal["plain", "gem", "forked"] = Field(default="gem", description="Wand tip style")
    gem_color: Literal["blue", "green", "red", "purple"] = Field(default="purple", description="Optional gem or magical accent color")

class OrbSchema(BaseModel):
    asset_type: Literal["orb"] = "orb"
    diameter: float = Field(default=24.0, ge=10.0, le=50.0, description="Orb diameter in centimeters")
    orb_material: Literal["crystal", "glass", "obsidian"] = Field(default="crystal", description="Material of the orb itself")
    glow_color: Literal["blue", "green", "red", "purple"] = Field(default="blue", description="Dominant magical glow color")
    has_stand: bool = Field(default=True, description="Whether the orb includes a stand or cradle")

class TableSchema(BaseModel):
    asset_type: Literal["table"] = "table"
    width: float = Field(default=120.0, ge=60.0, le=240.0, description="Tabletop width in centimeters")
    depth: float = Field(default=80.0, ge=40.0, le=150.0, description="Tabletop depth in centimeters")
    height: float = Field(default=75.0, ge=40.0, le=120.0, description="Total table height in centimeters")
    leg_style: Literal["square", "round"] = Field(default="square", description="Style of the table legs")

class DiningTableSchema(BaseModel):
    asset_type: Literal["dining_table"] = "dining_table"
    width: float = Field(default=180.0, ge=120.0, le=300.0, description="Tabletop long-side width in centimeters")
    depth: float = Field(default=90.0, ge=70.0, le=130.0, description="Tabletop short-side depth in centimeters")
    height: float = Field(default=78.0, ge=65.0, le=90.0, description="Total table height in centimeters")
    seats: int = Field(default=6, ge=4, le=12, description="Number of seats the table accommodates (affects width)")
    leg_style: Literal["square", "turned"] = Field(default="square", description="Style of the dining table legs")

class CoffeeTableSchema(BaseModel):
    asset_type: Literal["coffee_table"] = "coffee_table"
    width: float = Field(default=110.0, ge=60.0, le=160.0, description="Long-side width in centimeters")
    depth: float = Field(default=60.0, ge=40.0, le=90.0, description="Short-side depth in centimeters")
    height: float = Field(default=45.0, ge=30.0, le=60.0, description="Total table height in centimeters (low)")
    style: Literal["slab", "glass_frame"] = Field(default="slab", description="Top surface style")
    leg_style: Literal["block", "hairpin"] = Field(default="block", description="Style of the coffee table legs")

class BarrelSchema(BaseModel):
    asset_type: Literal["barrel"] = "barrel"
    radius: float = Field(default=0.4, ge=0.15, le=1.5, description="Barrel max radius in meters")
    height: float = Field(default=1.0, ge=0.3, le=3.0, description="Barrel height in meters")

class CrateSchema(BaseModel):
    asset_type: Literal["crate"] = "crate"
    width: float = Field(default=1.0, ge=0.2, le=3.0, description="Crate width in meters")
    depth: float = Field(default=1.0, ge=0.2, le=3.0, description="Crate depth in meters")
    height: float = Field(default=1.0, ge=0.2, le=3.0, description="Crate height in meters")

class ShieldSchema(BaseModel):
    asset_type: Literal["shield"] = "shield"
    shield_style: Literal["round", "heater"] = Field(default="round", description="Style shape of the shield")
    diameter: float = Field(default=60.0, ge=30.0, le=120.0, description="Shield diameter/width in centimeters")
    boss_material: Literal["steel", "brass", "wood"] = Field(default="steel", description="Material of the center boss dome")
    has_rim: bool = Field(default=True, description="Whether the shield has a metallic outer rim")

class ChairSchema(BaseModel):
    asset_type: Literal["chair"] = "chair"
    width: float = Field(default=50.0, ge=30.0, le=100.0, description="Seat width in centimeters")
    depth: float = Field(default=50.0, ge=30.0, le=100.0, description="Seat depth in centimeters")
    seat_height: float = Field(default=45.0, ge=30.0, le=80.0, description="Seat height from ground in centimeters")
    backrest_height: float = Field(default=50.0, ge=20.0, le=100.0, description="Backrest height above the seat in centimeters")
    leg_style: Literal["square", "round"] = Field(default="square", description="Style of the chair legs")

class DeskSchema(BaseModel):
    asset_type: Literal["desk"] = "desk"
    width: float = Field(default=140.0, ge=80.0, le=220.0, description="Desktop width in centimeters")
    depth: float = Field(default=70.0, ge=50.0, le=100.0, description="Desktop depth in centimeters")
    height: float = Field(default=75.0, ge=60.0, le=120.0, description="Total desk height in centimeters")
    style: Literal["straight", "l_shape", "standing"] = Field(default="straight", description="Desk layout style")
    has_drawers: bool = Field(default=False, description="Whether the desk has a side drawer pedestal")
    material: Literal["wood", "metal_wood", "white"] = Field(default="wood", description="Desk surface and frame material")

class StoolSchema(BaseModel):
    asset_type: Literal["stool"] = "stool"
    diameter: float = Field(default=35.0, ge=20.0, le=60.0, description="Seat diameter or width in centimeters")
    height: float = Field(default=65.0, ge=40.0, le=85.0, description="Total stool height in centimeters (counter/bar height)")
    style: Literal["round", "square", "saddle"] = Field(default="round", description="Seat shape style")
    num_legs: int = Field(default=3, ge=3, le=4, description="Number of legs (3 or 4)")
    has_footrest: bool = Field(default=True, description="Whether the stool has a mid-leg footrest ring")
    material: Literal["wood", "metal", "mixed"] = Field(default="wood", description="Stool material")

class ChestSchema(BaseModel):
    asset_type: Literal["chest"] = "chest"
    width: float = Field(default=80.0, ge=40.0, le=150.0, description="Chest width in centimeters")
    depth: float = Field(default=50.0, ge=30.0, le=100.0, description="Chest depth in centimeters")
    height: float = Field(default=50.0, ge=30.0, le=100.0, description="Total chest height in centimeters")
    lid_style: Literal["flat", "arched"] = Field(default="flat", description="Style shape of the chest lid")
    has_lock: bool = Field(default=True, description="Whether the chest has a lock on the front")

class AxeSchema(BaseModel):
    asset_type: Literal["axe"] = "axe"
    shaft_length: float = Field(default=80.0, ge=40.0, le=150.0, description="Axe shaft length in centimeters")
    axe_style: Literal["single", "double"] = Field(default="single", description="Whether single-headed or double-headed axe")
    head_material: Literal["steel", "brass"] = Field(default="steel", description="Material of the axe head blades")
    shaft_material: Literal["wood", "metal"] = Field(default="wood", description="Shaft handle material")

class HelmetSchema(BaseModel):
    asset_type: Literal["helmet"] = "helmet"
    style: Literal["knight", "spartan", "viking"] = Field(default="knight", description="Style design of the helmet")
    material: Literal["steel", "brass", "bronze"] = Field(default="steel", description="Material of the helmet body")
    has_crest: bool = Field(default=True, description="Whether the helmet has a top plume/crest or horns")

class TorchSchema(BaseModel):
    asset_type: Literal["torch"] = "torch"
    style: Literal["handheld", "wall_mounted"] = Field(default="handheld", description="Style of the torch mounting")
    shaft_length: float = Field(default=40.0, ge=20.0, le=100.0, description="Shaft handle length in centimeters")
    flame_size: float = Field(default=15.0, ge=5.0, le=30.0, description="Flame mesh scale/size in centimeters")

class SofaSchema(BaseModel):
    asset_type: Literal["sofa"] = "sofa"
    style: Literal["sofa", "couch", "armchair"] = Field(default="sofa", description="Sofa design style")
    width: float = Field(default=180.0, ge=80.0, le=240.0, description="Total width in centimeters")
    depth: float = Field(default=90.0, ge=60.0, le=120.0, description="Total depth in centimeters")
    has_armrests: bool = Field(default=True, description="Whether the sofa has side armrests")

class BenchSchema(BaseModel):
    asset_type: Literal["bench"] = "bench"
    width: float = Field(default=120.0, ge=80.0, le=250.0, description="Bench width in centimeters")
    depth: float = Field(default=40.0, ge=30.0, le=100.0, description="Bench depth in centimeters")
    height: float = Field(default=45.0, ge=30.0, le=80.0, description="Total bench height in centimeters")
    has_backrest: bool = Field(default=False, description="Whether the bench has a backrest")
    leg_style: Literal["straight", "x_frame"] = Field(default="straight", description="Style of the bench legs")
    material: Literal["wood", "metal", "cushioned"] = Field(default="wood", description="Bench material")

class CouchSchema(BaseModel):
    asset_type: Literal["couch"] = "couch"
    width: float = Field(default=200.0, ge=140.0, le=300.0, description="Couch width in centimeters")
    depth: float = Field(default=90.0, ge=70.0, le=130.0, description="Couch depth in centimeters")
    height: float = Field(default=85.0, ge=60.0, le=110.0, description="Total couch height in centimeters")
    has_chaise: bool = Field(default=False, description="Whether the couch has an L-shaped chaise lounge corner")
    material: Literal["fabric", "leather", "velvet"] = Field(default="fabric", description="Couch upholstery material")

class ArmchairSchema(BaseModel):
    asset_type: Literal["armchair"] = "armchair"
    width: float = Field(default=85.0, ge=60.0, le=130.0, description="Armchair width in centimeters")
    depth: float = Field(default=80.0, ge=60.0, le=110.0, description="Armchair depth in centimeters")
    height: float = Field(default=85.0, ge=65.0, le=110.0, description="Total armchair height in centimeters")
    style: Literal["classic", "modern", "recliner"] = Field(default="classic", description="Armchair style")
    material: Literal["fabric", "leather", "velvet"] = Field(default="fabric", description="Armchair upholstery material")

class BedSchema(BaseModel):
    asset_type: Literal["bed"] = "bed"
    width: float = Field(default=160.0, ge=90.0, le=220.0, description="Bed width in centimeters")
    depth: float = Field(default=200.0, ge=180.0, le=220.0, description="Bed depth in centimeters")
    height: float = Field(default=60.0, ge=30.0, le=100.0, description="Total bed height in centimeters")
    has_headboard: bool = Field(default=True, description="Whether the bed has a headboard")
    material: Literal["wood", "metal", "padded"] = Field(default="wood", description="Bed frame material")

class BunkBedSchema(BaseModel):
    asset_type: Literal["bunk_bed"] = "bunk_bed"
    width: float = Field(default=100.0, ge=80.0, le=140.0, description="Bunk bed width in centimeters")
    depth: float = Field(default=200.0, ge=180.0, le=220.0, description="Bunk bed depth in centimeters")
    height: float = Field(default=180.0, ge=140.0, le=220.0, description="Total bunk bed height in centimeters")
    has_ladder: bool = Field(default=True, description="Whether the bunk bed has a ladder")
    material: Literal["wood", "metal"] = Field(default="wood", description="Bunk bed frame material")

class WardrobeSchema(BaseModel):
    asset_type: Literal["wardrobe"] = "wardrobe"
    width: float = Field(default=120.0, ge=60.0, le=200.0, description="Wardrobe width in centimeters")
    depth: float = Field(default=60.0, ge=40.0, le=90.0, description="Wardrobe depth in centimeters")
    height: float = Field(default=190.0, ge=140.0, le=240.0, description="Total wardrobe height in centimeters")
    style: Literal["classic", "modern", "open"] = Field(default="classic", description="Wardrobe design style")
    has_mirror: bool = Field(default=False, description="Whether the wardrobe has a door mirror")

class StorageSchema(BaseModel):
    asset_type: Literal["storage"] = "storage"
    style: Literal["cabinet", "shelf", "wardrobe", "bookcase"] = Field(default="shelf", description="Storage cabinet design style")
    width: float = Field(default=100.0, ge=40.0, le=200.0, description="Storage width in centimeters")
    depth: float = Field(default=40.0, ge=30.0, le=80.0, description="Storage depth in centimeters")
    height: float = Field(default=160.0, ge=60.0, le=220.0, description="Storage height in centimeters")
    num_shelves: int = Field(default=3, ge=1, le=6, description="Number of shelves inside the storage unit")
    has_doors: bool = Field(default=False, description="Whether the storage unit has front doors")

class LightingSchema(BaseModel):
    asset_type: Literal["lighting"] = "lighting"
    style: Literal["lamp", "chandelier", "candle"] = Field(default="lamp", description="Lighting fixture style")
    height: float = Field(default=120.0, ge=10.0, le=200.0, description="Total height of the fixture in centimeters")
    is_lit: bool = Field(default=True, description="Whether the light/flame is lit")

class ClosetSchema(BaseModel):
    asset_type: Literal["closet"] = "closet"
    width: float = Field(default=150.0, ge=80.0, le=250.0, description="Closet width in centimeters")
    depth: float = Field(default=65.0, ge=50.0, le=100.0, description="Closet depth in centimeters")
    height: float = Field(default=200.0, ge=160.0, le=250.0, description="Total closet height in centimeters")
    door_style: Literal["sliding", "hinged", "walk_in"] = Field(default="hinged", description="Door style")
    doors: int = Field(default=2, ge=0, le=4, description="Number of doors (hinged/sliding)")
    material: Literal["wood", "white_laminate", "dark_oak"] = Field(default="wood", description="Closet material")

class DresserSchema(BaseModel):
    asset_type: Literal["dresser"] = "dresser"
    width: float = Field(default=120.0, ge=60.0, le=180.0, description="Dresser width in centimeters")
    depth: float = Field(default=50.0, ge=40.0, le=80.0, description="Dresser depth in centimeters")
    height: float = Field(default=90.0, ge=60.0, le=130.0, description="Total dresser height in centimeters")
    drawers_rows: int = Field(default=3, ge=2, le=5, description="Number of drawer rows")
    drawers_cols: int = Field(default=2, ge=1, le=3, description="Number of drawer columns")
    style: Literal["modern", "classic", "rustic"] = Field(default="classic", description="Dresser design style")

class CabinetSchema(BaseModel):
    asset_type: Literal["cabinet"] = "cabinet"
    width: float = Field(default=80.0, ge=40.0, le=150.0, description="Cabinet width in centimeters")
    depth: float = Field(default=40.0, ge=30.0, le=70.0, description="Cabinet depth in centimeters")
    height: float = Field(default=120.0, ge=60.0, le=200.0, description="Total cabinet height in centimeters")
    has_glass: bool = Field(default=False, description="Whether the cabinet doors have glass panes")
    shelves: int = Field(default=3, ge=1, le=5, description="Number of inside shelves")
    style: Literal["kitchen", "display", "credenza", "bathroom"] = Field(default="display", description="Cabinet style style")

# Discriminator pattern using Pydantic Union type
class ShelfSchema(BaseModel):
    asset_type: Literal["shelf"] = "shelf"
    width: float = Field(default=80.0, ge=40.0, le=150.0, description="Shelf width in centimeters")
    depth: float = Field(default=25.0, ge=15.0, le=45.0, description="Shelf depth in centimeters")
    height: float = Field(default=20.0, ge=10.0, le=40.0, description="Shelf height in centimeters")
    material: Literal["wood", "metal", "glass"] = Field(default="wood", description="Shelf board material")
    brackets: Literal["none", "floating", "industrial"] = Field(default="floating", description="Type of mounting brackets")

class BookcaseSchema(BaseModel):
    asset_type: Literal["bookcase"] = "bookcase"
    width: float = Field(default=90.0, ge=40.0, le=160.0, description="Bookcase width in centimeters")
    depth: float = Field(default=35.0, ge=25.0, le=60.0, description="Bookcase depth in centimeters")
    height: float = Field(default=180.0, ge=100.0, le=240.0, description="Total bookcase height in centimeters")
    shelves: int = Field(default=4, ge=2, le=7, description="Number of horizontal shelves")
    has_back_panel: bool = Field(default=True, description="Whether the bookcase has a back backing panel")
    material: Literal["wood", "painted_mdf", "metal_frame"] = Field(default="wood", description="Bookcase structural material")

class NightstandSchema(BaseModel):
    asset_type: Literal["nightstand"] = "nightstand"
    width: float = Field(default=50.0, ge=35.0, le=75.0, description="Nightstand width in centimeters")
    depth: float = Field(default=40.0, ge=30.0, le=60.0, description="Nightstand depth in centimeters")
    height: float = Field(default=60.0, ge=40.0, le=80.0, description="Nightstand height in centimeters")
    drawers: int = Field(default=1, ge=0, le=3, description="Number of drawers")
    has_open_shelf: bool = Field(default=True, description="Whether the nightstand has an open storage shelf compartment")
    style: Literal["modern", "classic", "mid_century"] = Field(default="modern", description="Nightstand style")

class TVStandSchema(BaseModel):
    asset_type: Literal["tv_stand"] = "tv_stand"
    width: float = Field(default=150.0, ge=100.0, le=220.0, description="TV stand width in centimeters")
    depth: float = Field(default=45.0, ge=35.0, le=60.0, description="TV stand depth in centimeters")
    height: float = Field(default=50.0, ge=30.0, le=85.0, description="TV stand height in centimeters")
    compartments: int = Field(default=3, ge=2, le=5, description="Number of storage compartments")
    has_doors: bool = Field(default=False, description="Whether the TV stand has compartment doors")
    style: Literal["modern", "industrial", "classic"] = Field(default="modern", description="TV stand design style")

class FridgeSchema(BaseModel):
    asset_type: Literal["fridge"] = "fridge"
    width: float = Field(default=75.0, ge=50.0, le=100.0, description="Refrigerator width in centimeters")
    depth: float = Field(default=70.0, ge=50.0, le=90.0, description="Refrigerator depth in centimeters")
    height: float = Field(default=180.0, ge=120.0, le=220.0, description="Refrigerator height in centimeters")
    style: Literal["single_door", "double_door", "french_door"] = Field(default="double_door", description="Door layout style")
    material: Literal["stainless_steel", "white", "black_matte"] = Field(default="stainless_steel", description="Finish material")
    has_dispenser: bool = Field(default=False, description="Whether the fridge has a water/ice dispenser on the door")

class StoveSchema(BaseModel):
    asset_type: Literal["stove"] = "stove"
    width: float = Field(default=75.0, ge=50.0, le=100.0, description="Stove cooktop width in centimeters")
    depth: float = Field(default=60.0, ge=50.0, le=80.0, description="Stove cooktop depth in centimeters")
    height: float = Field(default=90.0, ge=80.0, le=100.0, description="Total stove height in centimeters")
    burners: int = Field(default=4, ge=2, le=6, description="Number of burner rings")
    style: Literal["gas", "electric_glass"] = Field(default="gas", description="Stove heating style")
    material: Literal["stainless_steel", "black", "white"] = Field(default="stainless_steel", description="Stove body finish material")

class OvenSchema(BaseModel):
    asset_type: Literal["oven"] = "oven"
    width: float = Field(default=60.0, ge=50.0, le=90.0, description="Oven width in centimeters")
    depth: float = Field(default=55.0, ge=45.0, le=75.0, description="Oven depth in centimeters")
    height: float = Field(default=60.0, ge=45.0, le=90.0, description="Oven height in centimeters")
    has_glass_window: bool = Field(default=True, description="Whether the oven door has a glass viewing window")
    shelves: int = Field(default=2, ge=1, le=4, description="Number of wire rack shelves inside")
    style: Literal["built_in", "freestanding"] = Field(default="built_in", description="Oven installation style")

class MicrowaveSchema(BaseModel):
    asset_type: Literal["microwave"] = "microwave"
    width: float = Field(default=55.0, ge=40.0, le=70.0, description="Microwave width in centimeters")
    depth: float = Field(default=40.0, ge=30.0, le=50.0, description="Microwave depth in centimeters")
    height: float = Field(default=35.0, ge=25.0, le=45.0, description="Microwave height in centimeters")
    style: Literal["countertop", "built_in"] = Field(default="countertop", description="Microwave style placement")
    has_glass_door: bool = Field(default=True, description="Whether the microwave door has a viewing glass window")

class SinkSchema(BaseModel):
    asset_type: Literal["sink"] = "sink"
    width: float = Field(default=80.0, ge=45.0, le=120.0, description="Sink cabinet width in centimeters")
    depth: float = Field(default=60.0, ge=45.0, le=80.0, description="Sink cabinet depth in centimeters")
    height: float = Field(default=85.0, ge=70.0, le=100.0, description="Sink cabinet height in centimeters")
    style: Literal["single_basin", "double_basin", "pedestal", "wall_mounted"] = Field(default="single_basin", description="Sink style")
    faucet_style: Literal["goose_neck", "standard"] = Field(default="goose_neck", description="Faucet design shape")

class CountertopSchema(BaseModel):
    asset_type: Literal["countertop"] = "countertop"
    width: float = Field(default=120.0, ge=60.0, le=240.0, description="Countertop width in centimeters")
    depth: float = Field(default=60.0, ge=50.0, le=80.0, description="Countertop depth in centimeters")
    height: float = Field(default=90.0, ge=80.0, le=100.0, description="Countertop total height in centimeters")
    has_drawers: bool = Field(default=True, description="Whether base cabinet has drawer rows")
    has_backsplash: bool = Field(default=True, description="Whether countertop has back wall backsplash guard")
    material: Literal["marble", "granite", "wood"] = Field(default="marble", description="Countertop slab surface material")

class CupboardSchema(BaseModel):
    asset_type: Literal["cupboard"] = "cupboard"
    width: float = Field(default=100.0, ge=60.0, le=180.0, description="Cupboard width in centimeters")
    depth: float = Field(default=45.0, ge=35.0, le=70.0, description="Cupboard depth in centimeters")
    height: float = Field(default=180.0, ge=120.0, le=220.0, description="Total cupboard height in centimeters")
    style: Literal["hutch", "pantry"] = Field(default="hutch", description="Cupboard design style")
    has_drawers: bool = Field(default=True, description="Whether the cupboard has bottom drawers")
    shelves: int = Field(default=3, ge=1, le=5, description="Number of inside/upper shelves")

class KitchenIslandSchema(BaseModel):
    asset_type: Literal["kitchen_island"] = "kitchen_island"
    width: float = Field(default=160.0, ge=100.0, le=240.0, description="Kitchen island width in centimeters")
    depth: float = Field(default=90.0, ge=60.0, le=120.0, description="Kitchen island depth in centimeters")
    height: float = Field(default=90.0, ge=80.0, le=100.0, description="Kitchen island height in centimeters")
    overhang_depth: float = Field(default=25.0, ge=10.0, le=40.0, description="Overhang depth for seating in centimeters")
    has_stools: bool = Field(default=True, description="Whether the island comes with stools")
    stools_count: int = Field(default=2, ge=0, le=4, description="Number of matching bar stools under overhang")
    material: Literal["wood_marble", "industrial_metal"] = Field(default="wood_marble", description="Finish style style")

class DiningSetSchema(BaseModel):
    asset_type: Literal["dining_set"] = "dining_set"
    table_width: float = Field(default=180.0, ge=120.0, le=260.0, description="Table top width in centimeters")
    table_depth: float = Field(default=90.0, ge=70.0, le=120.0, description="Table top depth in centimeters")
    table_height: float = Field(default=75.0, ge=65.0, le=90.0, description="Table top height in centimeters")
    chair_count: int = Field(default=6, ge=2, le=10, description="Number of chairs in the dining set")
    chair_style: Literal["classic", "modern"] = Field(default="classic", description="Style design of chairs")
    material: Literal["oak", "walnut"] = Field(default="oak", description="Dining set material")

class ToiletSchema(BaseModel):
    asset_type: Literal["toilet"] = "toilet"
    width: float = Field(default=50.0, ge=35.0, le=70.0, description="Toilet width in centimeters")
    depth: float = Field(default=70.0, ge=55.0, le=90.0, description="Toilet depth in centimeters")
    height: float = Field(default=80.0, ge=65.0, le=95.0, description="Total toilet height in centimeters")
    bowl_shape: Literal["round", "elongated"] = Field(default="elongated", description="Shape of the toilet bowl")
    has_lid_open: bool = Field(default=False, description="Whether the toilet seat lid is open")
    tank_width: float = Field(default=45.0, ge=30.0, le=60.0, description="Water tank width in centimeters")
    tank_depth: float = Field(default=20.0, ge=15.0, le=30.0, description="Water tank depth in centimeters")

class BathtubSchema(BaseModel):
    asset_type: Literal["bathtub"] = "bathtub"
    width: float = Field(default=160.0, ge=120.0, le=200.0, description="Bathtub width/length in centimeters")
    depth: float = Field(default=75.0, ge=60.0, le=100.0, description="Bathtub depth in centimeters")
    height: float = Field(default=60.0, ge=45.0, le=80.0, description="Bathtub height in centimeters")
    style: Literal["freestanding", "alcove", "clawfoot"] = Field(default="freestanding", description="Bathtub style")
    material: Literal["ceramic", "copper", "stone"] = Field(default="ceramic", description="Bathtub construction material")
    has_faucet: bool = Field(default=True, description="Whether the bathtub has an attached faucet")

class ShowerSchema(BaseModel):
    asset_type: Literal["shower"] = "shower"
    width: float = Field(default=90.0, ge=70.0, le=150.0, description="Shower base width in centimeters")
    depth: float = Field(default=90.0, ge=70.0, le=150.0, description="Shower base depth in centimeters")
    height: float = Field(default=210.0, ge=180.0, le=240.0, description="Total shower frame height in centimeters")
    enclosure: Literal["glass_door", "curtain", "none"] = Field(default="glass_door", description="Enclosure layout style")
    head_type: Literal["rain", "standard", "handheld"] = Field(default="standard", description="Shower head type")
    material: Literal["chrome", "brass", "matte_black"] = Field(default="chrome", description="Plumbing fixture material")

class MirrorSchema(BaseModel):
    asset_type: Literal["mirror"] = "mirror"
    width: float = Field(default=60.0, ge=30.0, le=120.0, description="Mirror width/diameter in centimeters")
    height: float = Field(default=80.0, ge=30.0, le=150.0, description="Mirror height in centimeters")
    shape: Literal["rectangular", "circular", "oval"] = Field(default="rectangular", description="Mirror shape")
    border_style: Literal["metallic", "wood", "frameless"] = Field(default="metallic", description="Border frame style")
    border_color: Literal["gold", "chrome", "black", "wood"] = Field(default="black", description="Border frame color/finish")

class TowelRackSchema(BaseModel):
    asset_type: Literal["towel_rack"] = "towel_rack"
    width: float = Field(default=60.0, ge=30.0, le=120.0, description="Rack width in centimeters")
    depth: float = Field(default=15.0, ge=8.0, le=30.0, description="Rack depth in centimeters")
    height: float = Field(default=20.0, ge=10.0, le=60.0, description="Rack height in centimeters")
    bar_style: Literal["single_bar", "double_bar", "shelf_style"] = Field(default="single_bar", description="Style of the towel rack bars")
    material: Literal["chrome", "brass", "matte_black", "wood"] = Field(default="chrome", description="Rack bar material")
    has_towel: bool = Field(default=True, description="Whether a towel is hanging from the rack")
    towel_color: Literal["white", "blue", "gray", "green"] = Field(default="white", description="Color of the hanging towel")

class LampSchema(BaseModel):
    asset_type: Literal["lamp"] = "lamp"
    height: float = Field(default=60.0, ge=20.0, le=220.0, description="Total lamp height in centimeters")
    style: Literal["table", "floor"] = Field(default="table", description="Type of lamp (table or floor)")
    shade_shape: Literal["conical", "cylindrical"] = Field(default="conical", description="Shape of the lampshade")
    is_lit: bool = Field(default=True, description="Whether the lamp is switched on and glowing")

class ChandelierSchema(BaseModel):
    asset_type: Literal["chandelier"] = "chandelier"
    width: float = Field(default=80.0, ge=40.0, le=160.0, description="Total diameter/width in centimeters")
    height: float = Field(default=70.0, ge=30.0, le=150.0, description="Chandelier vertical height in centimeters")
    arms: int = Field(default=5, ge=3, le=12, description="Number of branches/arms holding lights")
    style: Literal["classic", "modern"] = Field(default="classic", description="Style of the chandelier")
    is_lit: bool = Field(default=True, description="Whether the chandelier is lit")

class PaintingSchema(BaseModel):
    asset_type: Literal["painting"] = "painting"
    width: float = Field(default=80.0, ge=30.0, le=200.0, description="Painting width in centimeters")
    height: float = Field(default=60.0, ge=30.0, le=200.0, description="Painting height in centimeters")
    frame_width: float = Field(default=3.0, ge=1.0, le=10.0, description="Frame border thickness/width in centimeters")
    style: Literal["landscape", "portrait", "square"] = Field(default="landscape", description="Overall aspect orientation")
    art_type: Literal["abstract", "minimalist", "geometric"] = Field(default="abstract", description="Style of painting art content")

class PictureFrameSchema(BaseModel):
    asset_type: Literal["picture_frame"] = "picture_frame"
    width: float = Field(default=40.0, ge=15.0, le=120.0, description="Frame outer width in centimeters")
    height: float = Field(default=50.0, ge=15.0, le=150.0, description="Frame outer height in centimeters")
    border_thickness: float = Field(default=2.5, ge=0.8, le=8.0, description="Border frame width in centimeters")
    style: Literal["classic", "modern"] = Field(default="modern", description="Border styling theme")
    has_matting: bool = Field(default=True, description="Whether a paper mat border (passepartout) is inside the frame")

class ClockSchema(BaseModel):
    asset_type: Literal["clock"] = "clock"
    width: float = Field(default=40.0, ge=20.0, le=120.0, description="Clock width/diameter in centimeters")
    height: float = Field(default=40.0, ge=20.0, le=120.0, description="Clock height in centimeters")
    depth: float = Field(default=5.0, ge=3.0, le=15.0, description="Clock depth in centimeters")
    shape: Literal["circular", "rectangular"] = Field(default="circular", description="Clock face shape")
    style: Literal["wall", "tabletop"] = Field(default="wall", description="Hanging wall clock or standing tabletop clock")
    material: Literal["wood", "metal", "plastic"] = Field(default="wood", description="Outer frame material")

class VaseSchema(BaseModel):
    asset_type: Literal["vase"] = "vase"
    height: float = Field(default=35.0, ge=15.0, le=80.0, description="Vase height in centimeters")
    diameter: float = Field(default=18.0, ge=10.0, le=40.0, description="Vase maximum outer diameter in centimeters")
    neck_diameter: float = Field(default=6.0, ge=3.0, le=15.0, description="Vase neck opening diameter in centimeters")
    style: Literal["classic", "modern", "geometric"] = Field(default="classic", description="Decorative visual style shape")
    material: Literal["ceramic", "glass", "clay"] = Field(default="ceramic", description="Vase material")

class PlantPotSchema(BaseModel):
    asset_type: Literal["plant_pot"] = "plant_pot"
    width: float = Field(default=30.0, ge=15.0, le=80.0, description="Pot width/diameter in centimeters")
    depth: float = Field(default=30.0, ge=15.0, le=80.0, description="Pot depth in centimeters")
    height: float = Field(default=30.0, ge=15.0, le=80.0, description="Pot height in centimeters")
    shape: Literal["cylindrical", "square", "rounded"] = Field(default="cylindrical", description="Plant pot base shape")
    material: Literal["terracotta", "ceramic", "plastic", "wood"] = Field(default="terracotta", description="Pot structure material")
    has_plant: bool = Field(default=True, description="Whether a leafy green plant grows out of the pot")

class RugSchema(BaseModel):
    asset_type: Literal["rug"] = "rug"
    width: float = Field(default=150.0, ge=60.0, le=400.0, description="Rug width in centimeters")
    depth: float = Field(default=100.0, ge=60.0, le=400.0, description="Rug depth/length in centimeters")
    thickness: float = Field(default=1.2, ge=0.5, le=5.0, description="Rug height/thickness in centimeters")
    shape: Literal["rectangular", "circular"] = Field(default="rectangular", description="Rug shape")
    pattern: Literal["solid", "geometric", "oriental", "striped"] = Field(default="geometric", description="Rug pattern design")
    color: Literal["cream", "red", "blue", "grey", "green"] = Field(default="cream", description="Primary rug color")

class WallSchema(BaseModel):
    asset_type: Literal["wall"] = "wall"
    width: float = Field(default=320.0, ge=120.0, le=1200.0, description="Wall span width in centimeters")
    height: float = Field(default=280.0, ge=240.0, le=400.0, description="Wall height in centimeters")
    thickness: float = Field(default=18.0, ge=10.0, le=50.0, description="Wall thickness in centimeters")
    material: Literal["brick", "concrete", "stone", "wood", "plaster"] = Field(default="plaster", description="Primary wall surface material")
    opening_type: Literal["none", "door", "window"] = Field(default="none", description="Optional wall opening type")
    opening_width: float = Field(default=110.0, ge=60.0, le=220.0, description="Opening width in centimeters when a door or window is present")
    opening_height: float = Field(default=190.0, ge=60.0, le=260.0, description="Opening height in centimeters when a door or window is present")
    has_trim: bool = Field(default=False, description="Whether the wall has decorative trim around the base or opening")

class FloorSchema(BaseModel):
    asset_type: Literal["floor"] = "floor"
    width: float = Field(default=420.0, ge=200.0, le=1600.0, description="Floor slab width in centimeters")
    depth: float = Field(default=420.0, ge=200.0, le=1600.0, description="Floor slab depth in centimeters")
    thickness: float = Field(default=20.0, ge=10.0, le=50.0, description="Floor slab thickness in centimeters")
    material: Literal["wood", "stone", "tile", "concrete"] = Field(default="wood", description="Primary floor finish material")
    tile_divisions: int = Field(default=6, ge=0, le=20, description="Number of visible plank or tile divisions across the surface")

class CeilingSchema(BaseModel):
    asset_type: Literal["ceiling"] = "ceiling"
    width: float = Field(default=420.0, ge=200.0, le=1600.0, description="Ceiling panel width in centimeters")
    depth: float = Field(default=420.0, ge=200.0, le=1600.0, description="Ceiling panel depth in centimeters")
    thickness: float = Field(default=12.0, ge=5.0, le=30.0, description="Ceiling thickness in centimeters")
    material: Literal["plaster", "wood", "concrete"] = Field(default="plaster", description="Primary ceiling material")
    has_trim: bool = Field(default=True, description="Whether the ceiling includes perimeter trim")

class RoofSchema(BaseModel):
    asset_type: Literal["roof"] = "roof"
    width: float = Field(default=520.0, ge=240.0, le=2000.0, description="Roof width in centimeters")
    depth: float = Field(default=420.0, ge=240.0, le=2000.0, description="Roof depth in centimeters")
    thickness: float = Field(default=18.0, ge=10.0, le=40.0, description="Roof panel thickness in centimeters")
    slope: float = Field(default=32.0, ge=15.0, le=60.0, description="Roof slope in degrees")
    roof_style: Literal["gabled", "flat", "hip", "mansard"] = Field(default="gabled", description="Overall roof form")
    overhang: float = Field(default=35.0, ge=0.0, le=100.0, description="Roof overhang distance in centimeters")
    material: Literal["clay_tiles", "wood_shingles", "metal_sheets"] = Field(default="clay_tiles", description="Roof cladding material")

class PillarSchema(BaseModel):
    asset_type: Literal["pillar"] = "pillar"
    height: float = Field(default=320.0, ge=200.0, le=800.0, description="Pillar height in centimeters")
    width: float = Field(default=40.0, ge=20.0, le=80.0, description="Pillar diameter or width in centimeters")
    shape: Literal["cylindrical", "square"] = Field(default="cylindrical", description="Pillar shaft profile")
    material: Literal["stone", "marble", "concrete", "wood"] = Field(default="stone", description="Pillar material")
    has_capital: bool = Field(default=True, description="Whether the pillar has a decorative capital and base")

class BeamSchema(BaseModel):
    asset_type: Literal["beam"] = "beam"
    length: float = Field(default=420.0, ge=100.0, le=2000.0, description="Beam span length in centimeters")
    width: float = Field(default=24.0, ge=10.0, le=60.0, description="Beam width in centimeters")
    height: float = Field(default=32.0, ge=10.0, le=80.0, description="Beam height in centimeters")
    material: Literal["wood", "steel", "concrete"] = Field(default="wood", description="Beam material")

class FoundationSchema(BaseModel):
    asset_type: Literal["foundation"] = "foundation"
    width: float = Field(default=720.0, ge=300.0, le=2400.0, description="Foundation slab width in centimeters")
    depth: float = Field(default=560.0, ge=300.0, le=2400.0, description="Foundation slab depth in centimeters")
    height: float = Field(default=70.0, ge=40.0, le=140.0, description="Foundation slab thickness in centimeters")
    footing_depth: float = Field(default=120.0, ge=50.0, le=300.0, description="Footing depth below the slab in centimeters")
    material: Literal["concrete", "stone"] = Field(default="concrete", description="Foundation material")
    has_footings: bool = Field(default=True, description="Whether the foundation includes visible footings")

class DoorSchema(BaseModel):
    asset_type: Literal["door"] = "door"
    width: float = Field(default=92.0, ge=80.0, le=120.0, description="Door width in centimeters")
    height: float = Field(default=210.0, ge=200.0, le=220.0, description="Door height in centimeters")
    thickness: float = Field(default=4.5, ge=3.0, le=6.0, description="Door thickness in centimeters")
    material: Literal["wood", "metal"] = Field(default="wood", description="Primary door material")
    panel_style: Literal["plain", "inset", "double"] = Field(default="inset", description="Door panel style")
    has_frame: bool = Field(default=True, description="Whether the door includes a surrounding frame")
    has_handle: bool = Field(default=True, description="Whether the door includes a visible handle")

class WindowSchema(BaseModel):
    asset_type: Literal["window"] = "window"
    width: float = Field(default=140.0, ge=60.0, le=200.0, description="Window width in centimeters")
    height: float = Field(default=120.0, ge=60.0, le=180.0, description="Window height in centimeters")
    thickness: float = Field(default=12.0, ge=6.0, le=20.0, description="Window frame depth in centimeters")
    frame_material: Literal["wood", "aluminum"] = Field(default="wood", description="Primary frame material")
    has_mullions: bool = Field(default=True, description="Whether the window includes mullions")
    has_sill: bool = Field(default=True, description="Whether the window includes a lower sill")

class ArchwaySchema(BaseModel):
    asset_type: Literal["archway"] = "archway"
    width: float = Field(default=220.0, ge=100.0, le=400.0, description="Clear arch opening width in centimeters")
    height: float = Field(default=280.0, ge=200.0, le=500.0, description="Overall arch height in centimeters")
    thickness: float = Field(default=28.0, ge=15.0, le=80.0, description="Arch wall thickness in centimeters")
    support_width: float = Field(default=34.0, ge=20.0, le=80.0, description="Width of each side support in centimeters")
    material: Literal["stone", "brick"] = Field(default="stone", description="Archway material")

class GateSchema(BaseModel):
    asset_type: Literal["gate"] = "gate"
    width: float = Field(default=220.0, ge=100.0, le=1000.0, description="Gate width in centimeters")
    height: float = Field(default=180.0, ge=100.0, le=500.0, description="Gate height in centimeters")
    thickness: float = Field(default=8.0, ge=4.0, le=20.0, description="Gate frame thickness in centimeters")
    material: Literal["wood", "iron"] = Field(default="iron", description="Primary gate material")
    gate_style: Literal["barred", "solid"] = Field(default="barred", description="Gate panel style")
    bar_count: int = Field(default=8, ge=3, le=16, description="Number of vertical bars or slats")

class StairsSchema(BaseModel):
    asset_type: Literal["stairs"] = "stairs"
    width: float = Field(default=120.0, ge=80.0, le=220.0, description="Stair width in centimeters")
    step_count: int = Field(default=8, ge=3, le=18, description="Number of steps")
    step_height: float = Field(default=17.0, ge=15.0, le=22.0, description="Height of each step in centimeters")
    step_depth: float = Field(default=28.0, ge=24.0, le=36.0, description="Depth of each step in centimeters")
    material: Literal["wood", "stone", "concrete"] = Field(default="wood", description="Primary stair material")
    has_railing: bool = Field(default=True, description="Whether the stairs include a railing")

class LadderSchema(BaseModel):
    asset_type: Literal["ladder"] = "ladder"
    width: float = Field(default=50.0, ge=40.0, le=60.0, description="Ladder width in centimeters")
    height: float = Field(default=260.0, ge=120.0, le=500.0, description="Overall ladder height in centimeters")
    rung_count: int = Field(default=8, ge=4, le=18, description="Number of ladder rungs")
    material: Literal["wood", "metal"] = Field(default="wood", description="Ladder material")

class RampSchema(BaseModel):
    asset_type: Literal["ramp"] = "ramp"
    width: float = Field(default=140.0, ge=80.0, le=500.0, description="Ramp width in centimeters")
    depth: float = Field(default=320.0, ge=120.0, le=1200.0, description="Ramp run length in centimeters")
    height: float = Field(default=55.0, ge=15.0, le=300.0, description="Ramp rise in centimeters")
    slope: float = Field(default=12.0, ge=5.0, le=30.0, description="Ramp incline in degrees")
    material: Literal["wood", "concrete", "stone"] = Field(default="concrete", description="Ramp material")
    has_side_curbs: bool = Field(default=True, description="Whether the ramp has low side curbs")

class BridgeSchema(BaseModel):
    asset_type: Literal["bridge"] = "bridge"
    length: float = Field(default=900.0, ge=200.0, le=10000.0, description="Bridge span length in centimeters")
    width: float = Field(default=220.0, ge=120.0, le=600.0, description="Bridge deck width in centimeters")
    height: float = Field(default=180.0, ge=60.0, le=800.0, description="Height from the lower ground to the deck in centimeters")
    deck_thickness: float = Field(default=24.0, ge=10.0, le=60.0, description="Bridge deck thickness in centimeters")
    material: Literal["wood", "stone", "steel"] = Field(default="wood", description="Bridge material")
    support_count: int = Field(default=4, ge=2, le=12, description="Number of support pillars")
    has_railings: bool = Field(default=True, description="Whether the bridge has side railings")

class BalconySchema(BaseModel):
    asset_type: Literal["balcony"] = "balcony"
    width: float = Field(default=320.0, ge=180.0, le=800.0, description="Balcony width in centimeters")
    depth: float = Field(default=160.0, ge=100.0, le=300.0, description="Balcony projection depth in centimeters")
    height: float = Field(default=105.0, ge=90.0, le=140.0, description="Balcony railing height in centimeters")
    thickness: float = Field(default=18.0, ge=10.0, le=40.0, description="Balcony slab thickness in centimeters")
    material: Literal["wood", "stone", "concrete"] = Field(default="concrete", description="Balcony material")
    has_railings: bool = Field(default=True, description="Whether the balcony includes railings")

class FenceSchema(BaseModel):
    asset_type: Literal["fence"] = "fence"
    width: float = Field(default=420.0, ge=120.0, le=1200.0, description="Fence run width in centimeters")
    height: float = Field(default=160.0, ge=100.0, le=300.0, description="Fence height in centimeters")
    thickness: float = Field(default=10.0, ge=4.0, le=20.0, description="Fence section thickness in centimeters")
    material: Literal["wood", "iron"] = Field(default="wood", description="Fence material")
    fence_style: Literal["picket", "panel"] = Field(default="picket", description="Fence section style")
    section_count: int = Field(default=10, ge=3, le=24, description="Number of repeated vertical sections")

class RailingSchema(BaseModel):
    asset_type: Literal["railing"] = "railing"
    width: float = Field(default=280.0, ge=120.0, le=1200.0, description="Railing span width in centimeters")
    height: float = Field(default=105.0, ge=90.0, le=120.0, description="Railing height in centimeters")
    depth: float = Field(default=14.0, ge=8.0, le=30.0, description="Railing depth in centimeters")
    material: Literal["wood", "steel"] = Field(default="steel", description="Railing material")
    baluster_count: int = Field(default=8, ge=3, le=24, description="Number of vertical balusters")

class ChimneySchema(BaseModel):
    asset_type: Literal["chimney"] = "chimney"
    width: float = Field(default=90.0, ge=40.0, le=180.0, description="Chimney width in centimeters")
    depth: float = Field(default=90.0, ge=40.0, le=180.0, description="Chimney depth in centimeters")
    height: float = Field(default=240.0, ge=100.0, le=500.0, description="Visible chimney height in centimeters")
    material: Literal["brick", "stone"] = Field(default="brick", description="Chimney material")
    has_cap: bool = Field(default=True, description="Whether the chimney has a cap")

class PorchSchema(BaseModel):
    asset_type: Literal["porch"] = "porch"
    width: float = Field(default=360.0, ge=200.0, le=600.0, description="Porch width in centimeters")
    depth: float = Field(default=220.0, ge=100.0, le=400.0, description="Porch depth in centimeters")
    height: float = Field(default=260.0, ge=220.0, le=360.0, description="Porch roof support height in centimeters")
    material: Literal["wood", "stone", "concrete"] = Field(default="wood", description="Porch material")
    pillar_count: int = Field(default=4, ge=2, le=6, description="Number of support pillars")
    has_steps: bool = Field(default=True, description="Whether the porch includes front steps")

class OakTreeSchema(BaseModel):
    asset_type: Literal["oak_tree"] = "oak_tree"
    height: float = Field(default=540.0, ge=320.0, le=1200.0, description="Overall tree height in centimeters")
    canopy_width: float = Field(default=420.0, ge=180.0, le=900.0, description="Canopy spread width in centimeters")
    trunk_radius: float = Field(default=22.0, ge=8.0, le=60.0, description="Trunk radius in centimeters")

class PineTreeSchema(BaseModel):
    asset_type: Literal["pine_tree"] = "pine_tree"
    height: float = Field(default=680.0, ge=400.0, le=1400.0, description="Overall tree height in centimeters")
    canopy_width: float = Field(default=260.0, ge=120.0, le=500.0, description="Maximum foliage width in centimeters")
    trunk_radius: float = Field(default=16.0, ge=6.0, le=40.0, description="Trunk radius in centimeters")
    layers: int = Field(default=5, ge=3, le=8, description="Number of conifer foliage layers")

class BirchTreeSchema(BaseModel):
    asset_type: Literal["birch_tree"] = "birch_tree"
    height: float = Field(default=560.0, ge=300.0, le=1100.0, description="Overall tree height in centimeters")
    canopy_width: float = Field(default=280.0, ge=120.0, le=420.0, description="Canopy spread width in centimeters")
    trunk_radius: float = Field(default=12.0, ge=5.0, le=30.0, description="Trunk radius in centimeters")

class PalmTreeSchema(BaseModel):
    asset_type: Literal["palm_tree"] = "palm_tree"
    height: float = Field(default=620.0, ge=300.0, le=1000.0, description="Overall palm height in centimeters")
    frond_span: float = Field(default=260.0, ge=120.0, le=500.0, description="Tip-to-tip frond span in centimeters")
    trunk_radius: float = Field(default=14.0, ge=6.0, le=30.0, description="Trunk radius in centimeters")

class DeadTreeSchema(BaseModel):
    asset_type: Literal["dead_tree"] = "dead_tree"
    height: float = Field(default=520.0, ge=250.0, le=900.0, description="Overall dead tree height in centimeters")
    branch_count: int = Field(default=7, ge=3, le=12, description="Number of bare branch limbs")
    trunk_radius: float = Field(default=16.0, ge=6.0, le=40.0, description="Trunk radius in centimeters")

class SaplingSchema(BaseModel):
    asset_type: Literal["sapling"] = "sapling"
    height: float = Field(default=180.0, ge=40.0, le=250.0, description="Young tree height in centimeters")
    canopy_width: float = Field(default=90.0, ge=20.0, le=140.0, description="Leaf canopy width in centimeters")

class GrassSchema(BaseModel):
    asset_type: Literal["grass"] = "grass"
    width: float = Field(default=110.0, ge=40.0, le=200.0, description="Patch width in centimeters")
    height: float = Field(default=34.0, ge=10.0, le=60.0, description="Grass blade height in centimeters")
    density: int = Field(default=28, ge=8, le=60, description="Approximate blade count density")

class BushSchema(BaseModel):
    asset_type: Literal["bush"] = "bush"
    width: float = Field(default=160.0, ge=60.0, le=240.0, description="Bush width in centimeters")
    height: float = Field(default=95.0, ge=40.0, le=160.0, description="Bush height in centimeters")
    density: int = Field(default=8, ge=5, le=18, description="Leaf cluster density")

class ShrubSchema(BaseModel):
    asset_type: Literal["shrub"] = "shrub"
    width: float = Field(default=150.0, ge=60.0, le=240.0, description="Shrub width in centimeters")
    height: float = Field(default=130.0, ge=60.0, le=220.0, description="Shrub height in centimeters")
    stems: int = Field(default=5, ge=3, le=12, description="Number of woody stems")

class FernSchema(BaseModel):
    asset_type: Literal["fern"] = "fern"
    width: float = Field(default=120.0, ge=40.0, le=180.0, description="Fern spread width in centimeters")
    height: float = Field(default=75.0, ge=30.0, le=120.0, description="Fern height in centimeters")
    fronds: int = Field(default=6, ge=4, le=12, description="Number of arching fronds")

class FlowerSchema(BaseModel):
    asset_type: Literal["flower"] = "flower"
    height: float = Field(default=45.0, ge=15.0, le=90.0, description="Flower stem height in centimeters")
    petals: int = Field(default=6, ge=4, le=16, description="Number of visible petals")
    bloom_color: Literal["pink", "yellow"] = Field(default="pink", description="Primary bloom color")

class MossSchema(BaseModel):
    asset_type: Literal["moss"] = "moss"
    width: float = Field(default=130.0, ge=40.0, le=200.0, description="Moss patch width in centimeters")
    depth: float = Field(default=100.0, ge=30.0, le=180.0, description="Moss patch depth in centimeters")
    thickness: float = Field(default=18.0, ge=4.0, le=30.0, description="Moss cushion thickness in centimeters")

class SmallRockSchema(BaseModel):
    asset_type: Literal["small_rock"] = "small_rock"
    width: float = Field(default=55.0, ge=15.0, le=120.0, description="Rock width in centimeters")
    depth: float = Field(default=45.0, ge=12.0, le=100.0, description="Rock depth in centimeters")
    height: float = Field(default=32.0, ge=10.0, le=80.0, description="Rock height in centimeters")

class BoulderSchema(BaseModel):
    asset_type: Literal["boulder"] = "boulder"
    width: float = Field(default=180.0, ge=80.0, le=320.0, description="Boulder width in centimeters")
    depth: float = Field(default=140.0, ge=60.0, le=260.0, description="Boulder depth in centimeters")
    height: float = Field(default=120.0, ge=50.0, le=220.0, description="Boulder height in centimeters")

class RockClusterSchema(BaseModel):
    asset_type: Literal["rock_cluster"] = "rock_cluster"
    width: float = Field(default=180.0, ge=60.0, le=320.0, description="Overall cluster width in centimeters")
    depth: float = Field(default=120.0, ge=40.0, le=240.0, description="Overall cluster depth in centimeters")
    rocks: int = Field(default=5, ge=3, le=12, description="Number of grouped rocks")

class CliffSectionSchema(BaseModel):
    asset_type: Literal["cliff_section"] = "cliff_section"
    width: float = Field(default=280.0, ge=120.0, le=500.0, description="Cliff face width in centimeters")
    depth: float = Field(default=140.0, ge=60.0, le=260.0, description="Cliff thickness/depth in centimeters")
    height: float = Field(default=300.0, ge=120.0, le=520.0, description="Cliff height in centimeters")

class LogSchema(BaseModel):
    asset_type: Literal["log"] = "log"
    length: float = Field(default=220.0, ge=60.0, le=500.0, description="Log length in centimeters")
    radius: float = Field(default=24.0, ge=6.0, le=60.0, description="Log radius in centimeters")

class TreeStumpSchema(BaseModel):
    asset_type: Literal["tree_stump"] = "tree_stump"
    radius: float = Field(default=38.0, ge=10.0, le=90.0, description="Stump radius in centimeters")
    height: float = Field(default=48.0, ge=10.0, le=120.0, description="Stump height in centimeters")

class FallenTreeSchema(BaseModel):
    asset_type: Literal["fallen_tree"] = "fallen_tree"
    length: float = Field(default=360.0, ge=120.0, le=700.0, description="Fallen tree trunk length in centimeters")
    trunk_radius: float = Field(default=20.0, ge=6.0, le=50.0, description="Trunk radius in centimeters")
    has_leaves: bool = Field(default=True, description="Whether sparse foliage remains attached")

class MushroomSchema(BaseModel):
    asset_type: Literal["mushroom"] = "mushroom"
    cap_diameter: float = Field(default=36.0, ge=8.0, le=80.0, description="Mushroom cap diameter in centimeters")
    height: float = Field(default=34.0, ge=6.0, le=80.0, description="Overall mushroom height in centimeters")

class VineSchema(BaseModel):
    asset_type: Literal["vine"] = "vine"
    length: float = Field(default=260.0, ge=60.0, le=600.0, description="Vine length in centimeters")
    leaf_density: int = Field(default=9, ge=3, le=20, description="Number of visible leaf groupings")

class RootSchema(BaseModel):
    asset_type: Literal["root"] = "root"
    width: float = Field(default=180.0, ge=60.0, le=320.0, description="Root spread width in centimeters")
    depth: float = Field(default=120.0, ge=40.0, le=240.0, description="Root spread depth in centimeters")
    height: float = Field(default=50.0, ge=10.0, le=120.0, description="Maximum exposed root height in centimeters")

class PondSchema(BaseModel):
    asset_type: Literal["pond"] = "pond"
    width: float = Field(default=240.0, ge=100.0, le=420.0, description="Pond width in centimeters")
    depth: float = Field(default=180.0, ge=80.0, le=340.0, description="Pond depth in centimeters")
    bank_height: float = Field(default=22.0, ge=6.0, le=60.0, description="Raised bank height in centimeters")

class RiverSegmentSchema(BaseModel):
    asset_type: Literal["river_segment"] = "river_segment"
    width: float = Field(default=160.0, ge=60.0, le=300.0, description="River water width in centimeters")
    length: float = Field(default=340.0, ge=120.0, le=700.0, description="Visible river segment length in centimeters")
    curve: float = Field(default=60.0, ge=0.0, le=180.0, description="Sideways river bend amount in centimeters")

class WaterfallSchema(BaseModel):
    asset_type: Literal["waterfall"] = "waterfall"
    width: float = Field(default=140.0, ge=60.0, le=260.0, description="Waterfall width in centimeters")
    height: float = Field(default=260.0, ge=80.0, le=500.0, description="Waterfall drop height in centimeters")
    pool_radius: float = Field(default=110.0, ge=40.0, le=240.0, description="Pool radius in centimeters")

class StreamSchema(BaseModel):
    asset_type: Literal["stream"] = "stream"
    width: float = Field(default=75.0, ge=20.0, le=160.0, description="Stream width in centimeters")
    length: float = Field(default=260.0, ge=80.0, le=500.0, description="Visible stream length in centimeters")
    curve: float = Field(default=36.0, ge=0.0, le=120.0, description="Sideways stream bend amount in centimeters")

class ChestplateSchema(BaseModel):
    asset_type: Literal["chestplate"] = "chestplate"
    width: float = Field(default=58.0, ge=40.0, le=90.0, description="Chestplate shoulder width in centimeters")
    height: float = Field(default=72.0, ge=45.0, le=110.0, description="Chestplate total torso height in centimeters")
    depth: float = Field(default=28.0, ge=15.0, le=45.0, description="Chestplate front-to-back depth in centimeters")
    material: Literal["steel", "iron", "bronze", "leather"] = Field(default="steel", description="Primary chestplate material")
    style: Literal["knight", "breastplate", "fantasy"] = Field(default="knight", description="Overall chestplate styling")

class GauntletsSchema(BaseModel):
    asset_type: Literal["gauntlets"] = "gauntlets"
    width: float = Field(default=34.0, ge=18.0, le=70.0, description="Combined pair width in centimeters")
    depth: float = Field(default=20.0, ge=10.0, le=40.0, description="Gauntlet hand depth in centimeters")
    height: float = Field(default=28.0, ge=15.0, le=55.0, description="Gauntlet cuff-to-hand height in centimeters")
    material: Literal["steel", "iron", "bronze", "leather"] = Field(default="steel", description="Primary gauntlet material")
    style: Literal["plate", "leather", "spiked"] = Field(default="plate", description="Gauntlet style silhouette")

class BootsSchema(BaseModel):
    asset_type: Literal["boots"] = "boots"
    width: float = Field(default=30.0, ge=18.0, le=60.0, description="Combined pair width in centimeters")
    depth: float = Field(default=40.0, ge=22.0, le=70.0, description="Boot toe-to-heel depth in centimeters")
    height: float = Field(default=46.0, ge=20.0, le=80.0, description="Boot shaft height in centimeters")
    material: Literal["leather", "steel", "iron"] = Field(default="leather", description="Primary boot material")
    style: Literal["travel", "plate", "riding"] = Field(default="travel", description="Boot style")

class BackpackSchema(BaseModel):
    asset_type: Literal["backpack"] = "backpack"
    width: float = Field(default=42.0, ge=24.0, le=80.0, description="Backpack width in centimeters")
    depth: float = Field(default=22.0, ge=14.0, le=45.0, description="Backpack depth in centimeters")
    height: float = Field(default=56.0, ge=30.0, le=90.0, description="Backpack height in centimeters")
    material: Literal["cloth", "leather", "canvas"] = Field(default="canvas", description="Primary pack fabric material")
    has_bedroll: bool = Field(default=False, description="Whether a rolled bedroll is strapped to the pack")

class BeltSchema(BaseModel):
    asset_type: Literal["belt"] = "belt"
    width: float = Field(default=110.0, ge=60.0, le=160.0, description="Belt overall length in centimeters")
    depth: float = Field(default=4.0, ge=2.0, le=12.0, description="Belt leather thickness in centimeters")
    height: float = Field(default=10.0, ge=4.0, le=18.0, description="Belt strap height in centimeters")
    material: Literal["leather", "cloth"] = Field(default="leather", description="Primary strap material")
    buckle_material: Literal["steel", "brass", "iron"] = Field(default="brass", description="Buckle metal material")

class PouchSchema(BaseModel):
    asset_type: Literal["pouch"] = "pouch"
    width: float = Field(default=20.0, ge=10.0, le=40.0, description="Pouch width in centimeters")
    depth: float = Field(default=12.0, ge=6.0, le=25.0, description="Pouch depth in centimeters")
    height: float = Field(default=22.0, ge=12.0, le=40.0, description="Pouch height in centimeters")
    material: Literal["leather", "cloth"] = Field(default="leather", description="Pouch body material")
    clasp_material: Literal["steel", "brass", "bone"] = Field(default="brass", description="Clasp or closure material")

class CapeSchema(BaseModel):
    asset_type: Literal["cape"] = "cape"
    width: float = Field(default=120.0, ge=60.0, le=200.0, description="Cape shoulder spread width in centimeters")
    height: float = Field(default=170.0, ge=90.0, le=240.0, description="Cape hanging length in centimeters")
    thickness: float = Field(default=1.5, ge=0.5, le=6.0, description="Cape fabric thickness in centimeters")
    fabric: Literal["red", "blue", "green", "black", "brown"] = Field(default="red", description="Primary cape fabric color")
    clasp_material: Literal["steel", "brass", "gold"] = Field(default="brass", description="Neck clasp material")

class TentSchema(BaseModel):
    asset_type: Literal["tent"] = "tent"
    width: float = Field(default=240.0, ge=120.0, le=500.0, description="Tent width in centimeters")
    depth: float = Field(default=280.0, ge=120.0, le=500.0, description="Tent depth in centimeters")
    height: float = Field(default=165.0, ge=90.0, le=280.0, description="Tent ridge height in centimeters")
    material: Literal["canvas", "cloth", "hide"] = Field(default="canvas", description="Tent fabric material")
    tent_style: Literal["ridge", "pup", "a_frame"] = Field(default="ridge", description="Tent silhouette type")

class CampfireSchema(BaseModel):
    asset_type: Literal["campfire"] = "campfire"
    width: float = Field(default=90.0, ge=40.0, le=200.0, description="Campfire footprint width in centimeters")
    depth: float = Field(default=90.0, ge=40.0, le=200.0, description="Campfire footprint depth in centimeters")
    height: float = Field(default=34.0, ge=12.0, le=90.0, description="Campfire flame or stacked-log height in centimeters")
    log_count: int = Field(default=5, ge=3, le=10, description="Number of visible stacked logs")
    is_lit: bool = Field(default=True, description="Whether the campfire is visibly lit")

class SleepingBagSchema(BaseModel):
    asset_type: Literal["sleeping_bag"] = "sleeping_bag"
    width: float = Field(default=78.0, ge=45.0, le=140.0, description="Sleeping bag width in centimeters")
    depth: float = Field(default=190.0, ge=120.0, le=260.0, description="Sleeping bag length in centimeters")
    thickness: float = Field(default=14.0, ge=4.0, le=30.0, description="Sleeping bag loft thickness in centimeters")
    fabric: Literal["blue", "green", "red", "brown", "gray"] = Field(default="blue", description="Sleeping bag fabric color")

class LanternSchema(BaseModel):
    asset_type: Literal["lantern"] = "lantern"
    width: float = Field(default=24.0, ge=12.0, le=60.0, description="Lantern width in centimeters")
    depth: float = Field(default=18.0, ge=12.0, le=60.0, description="Lantern depth in centimeters")
    height: float = Field(default=42.0, ge=20.0, le=90.0, description="Lantern total height in centimeters")
    material: Literal["iron", "brass", "steel"] = Field(default="iron", description="Lantern frame material")
    is_lit: bool = Field(default=True, description="Whether the lantern contains a visible flame")

class CookingPotSchema(BaseModel):
    asset_type: Literal["cooking_pot"] = "cooking_pot"
    diameter: float = Field(default=38.0, ge=18.0, le=90.0, description="Cooking pot diameter in centimeters")
    height: float = Field(default=28.0, ge=15.0, le=70.0, description="Cooking pot height in centimeters")
    material: Literal["iron", "steel", "copper"] = Field(default="iron", description="Cooking pot body material")
    has_lid: bool = Field(default=True, description="Whether the pot includes a lid")

class SupplyBoxSchema(BaseModel):
    asset_type: Literal["supply_box"] = "supply_box"
    width: float = Field(default=76.0, ge=30.0, le=160.0, description="Supply box width in centimeters")
    depth: float = Field(default=46.0, ge=20.0, le=100.0, description="Supply box depth in centimeters")
    height: float = Field(default=48.0, ge=20.0, le=90.0, description="Supply box height in centimeters")
    material: Literal["wood", "metal", "canvas"] = Field(default="wood", description="Supply box primary material")
    has_rope: bool = Field(default=True, description="Whether rope handles or bindings are present")

class CastleWallSchema(BaseModel):
    asset_type: Literal["castle_wall"] = "castle_wall"
    width: float = Field(default=420.0, ge=180.0, le=800.0, description="Castle wall section width in centimeters")
    thickness: float = Field(default=70.0, ge=30.0, le=180.0, description="Castle wall thickness in centimeters")
    height: float = Field(default=320.0, ge=180.0, le=520.0, description="Castle wall height in centimeters")
    material: Literal["stone", "brick"] = Field(default="stone", description="Castle wall construction material")
    has_crenellations: bool = Field(default=True, description="Whether battlement crenellations are included")

class TowerSchema(BaseModel):
    asset_type: Literal["tower"] = "tower"
    diameter: float = Field(default=320.0, ge=160.0, le=700.0, description="Tower diameter in centimeters")
    height: float = Field(default=620.0, ge=300.0, le=1200.0, description="Tower height in centimeters")
    material: Literal["stone", "brick"] = Field(default="stone", description="Tower wall material")
    roof_style: Literal["cone", "flat", "battlement"] = Field(default="battlement", description="Tower roof or crown style")

class DrawbridgeSchema(BaseModel):
    asset_type: Literal["drawbridge"] = "drawbridge"
    width: float = Field(default=260.0, ge=160.0, le=500.0, description="Drawbridge usable width in centimeters")
    length: float = Field(default=420.0, ge=200.0, le=900.0, description="Drawbridge span length in centimeters")
    thickness: float = Field(default=24.0, ge=12.0, le=80.0, description="Drawbridge deck thickness in centimeters")
    material: Literal["wood", "iron"] = Field(default="wood", description="Primary drawbridge material")
    chain_count: int = Field(default=2, ge=2, le=4, description="Number of visible lifting chains")

class ThroneSchema(BaseModel):
    asset_type: Literal["throne"] = "throne"
    width: float = Field(default=105.0, ge=60.0, le=200.0, description="Throne width in centimeters")
    depth: float = Field(default=90.0, ge=60.0, le=180.0, description="Throne depth in centimeters")
    height: float = Field(default=190.0, ge=120.0, le=300.0, description="Throne total height in centimeters")
    material: Literal["wood", "stone", "gold"] = Field(default="wood", description="Primary throne material")
    has_cushion: bool = Field(default=True, description="Whether the throne includes a seat cushion")

class BannerSchema(BaseModel):
    asset_type: Literal["banner"] = "banner"
    width: float = Field(default=70.0, ge=30.0, le=180.0, description="Banner cloth width in centimeters")
    height: float = Field(default=180.0, ge=80.0, le=360.0, description="Banner pole height in centimeters")
    fabric: Literal["red", "blue", "green", "black", "gold"] = Field(default="red", description="Banner fabric color")
    pole_material: Literal["wood", "steel", "brass"] = Field(default="wood", description="Banner pole material")

class MarketStallSchema(BaseModel):
    asset_type: Literal["market_stall"] = "market_stall"
    width: float = Field(default=260.0, ge=120.0, le=500.0, description="Market stall width in centimeters")
    depth: float = Field(default=180.0, ge=100.0, le=360.0, description="Market stall depth in centimeters")
    height: float = Field(default=250.0, ge=180.0, le=420.0, description="Market stall height in centimeters")
    frame_material: Literal["wood", "darkwood"] = Field(default="wood", description="Stall frame material")
    canopy_color: Literal["red", "blue", "green", "striped"] = Field(default="striped", description="Stall canopy color treatment")

class WellSchema(BaseModel):
    asset_type: Literal["well"] = "well"
    diameter: float = Field(default=150.0, ge=80.0, le=260.0, description="Well outer diameter in centimeters")
    height: float = Field(default=160.0, ge=100.0, le=260.0, description="Well total above-ground height in centimeters")
    material: Literal["stone", "brick", "wood"] = Field(default="stone", description="Well wall material")
    roof_style: Literal["none", "gable", "flat"] = Field(default="gable", description="Well roof style")

class CartSchema(BaseModel):
    asset_type: Literal["cart"] = "cart"
    width: float = Field(default=170.0, ge=100.0, le=320.0, description="Cart width in centimeters")
    depth: float = Field(default=260.0, ge=160.0, le=500.0, description="Cart length/depth in centimeters")
    height: float = Field(default=150.0, ge=80.0, le=220.0, description="Cart total height in centimeters")
    material: Literal["wood", "darkwood"] = Field(default="wood", description="Cart frame material")
    has_canopy: bool = Field(default=False, description="Whether the cart has a cloth canopy")

class AnvilSchema(BaseModel):
    asset_type: Literal["anvil"] = "anvil"
    width: float = Field(default=62.0, ge=30.0, le=120.0, description="Anvil top width in centimeters")
    depth: float = Field(default=28.0, ge=18.0, le=60.0, description="Anvil depth in centimeters")
    height: float = Field(default=42.0, ge=20.0, le=80.0, description="Anvil height in centimeters")
    material: Literal["iron", "steel"] = Field(default="iron", description="Anvil material")

class ForgeSchema(BaseModel):
    asset_type: Literal["forge"] = "forge"
    width: float = Field(default=220.0, ge=120.0, le=360.0, description="Forge width in centimeters")
    depth: float = Field(default=150.0, ge=100.0, le=260.0, description="Forge depth in centimeters")
    height: float = Field(default=130.0, ge=90.0, le=220.0, description="Forge height in centimeters")
    material: Literal["stone", "brick", "iron"] = Field(default="stone", description="Forge structure material")
    is_lit: bool = Field(default=True, description="Whether the forge fire is active")

class ControlPanelSchema(BaseModel):
    asset_type: Literal["control_panel"] = "control_panel"
    width: float = Field(default=140.0, ge=80.0, le=260.0, description="Control panel width in centimeters")
    depth: float = Field(default=80.0, ge=40.0, le=180.0, description="Control panel depth in centimeters")
    height: float = Field(default=110.0, ge=60.0, le=180.0, description="Control panel height in centimeters")
    material: Literal["steel", "darksteel", "aluminum"] = Field(default="darksteel", description="Primary panel body material")
    accent_color: Literal["blue", "cyan", "green", "red", "yellow", "purple", "white"] = Field(default="cyan", description="Screen and control accent color")
    screen_count: int = Field(default=4, ge=2, le=8, description="Number of visible display screens")

class TerminalSchema(BaseModel):
    asset_type: Literal["terminal"] = "terminal"
    width: float = Field(default=90.0, ge=50.0, le=180.0, description="Terminal width in centimeters")
    depth: float = Field(default=70.0, ge=35.0, le=140.0, description="Terminal depth in centimeters")
    height: float = Field(default=185.0, ge=100.0, le=280.0, description="Terminal height in centimeters")
    material: Literal["steel", "darksteel", "aluminum"] = Field(default="steel", description="Terminal housing material")
    accent_color: Literal["blue", "cyan", "green", "red", "yellow", "purple", "white"] = Field(default="green", description="Screen and control accent color")
    terminal_style: Literal["upright", "wall"] = Field(default="upright", description="Terminal mounting style")

class ComputerSchema(BaseModel):
    asset_type: Literal["computer"] = "computer"
    width: float = Field(default=95.0, ge=45.0, le=160.0, description="Computer setup width in centimeters")
    depth: float = Field(default=60.0, ge=30.0, le=110.0, description="Computer setup depth in centimeters")
    height: float = Field(default=70.0, ge=20.0, le=140.0, description="Computer setup height in centimeters")
    material: Literal["plastic_dark", "plastic_white", "aluminum"] = Field(default="plastic_dark", description="Computer body material")
    accent_color: Literal["blue", "cyan", "green", "red", "yellow", "purple", "white"] = Field(default="blue", description="Display light color")
    computer_style: Literal["desktop", "laptop"] = Field(default="desktop", description="Computer form factor")

class ServerRackSchema(BaseModel):
    asset_type: Literal["server_rack"] = "server_rack"
    width: float = Field(default=80.0, ge=50.0, le=160.0, description="Server rack width in centimeters")
    depth: float = Field(default=95.0, ge=50.0, le=180.0, description="Server rack depth in centimeters")
    height: float = Field(default=220.0, ge=120.0, le=320.0, description="Server rack height in centimeters")
    material: Literal["steel", "darksteel", "aluminum"] = Field(default="darksteel", description="Rack frame material")
    accent_color: Literal["blue", "cyan", "green", "red", "yellow", "purple", "white"] = Field(default="green", description="Indicator light color")
    rack_units: int = Field(default=12, ge=6, le=24, description="Number of server units represented")

class EnergyCellSchema(BaseModel):
    asset_type: Literal["energy_cell"] = "energy_cell"
    diameter: float = Field(default=26.0, ge=12.0, le=60.0, description="Energy cell diameter in centimeters")
    height: float = Field(default=60.0, ge=20.0, le=140.0, description="Energy cell height in centimeters")
    material: Literal["steel", "darksteel", "aluminum"] = Field(default="steel", description="Energy cell shell material")
    accent_color: Literal["blue", "cyan", "green", "red", "yellow", "purple", "white"] = Field(default="cyan", description="Core energy glow color")

class TechCrateSchema(BaseModel):
    asset_type: Literal["tech_crate"] = "tech_crate"
    width: float = Field(default=100.0, ge=40.0, le=220.0, description="Tech crate width in centimeters")
    depth: float = Field(default=70.0, ge=30.0, le=180.0, description="Tech crate depth in centimeters")
    height: float = Field(default=70.0, ge=25.0, le=180.0, description="Tech crate height in centimeters")
    material: Literal["steel", "darksteel", "aluminum"] = Field(default="darksteel", description="Crate shell material")
    accent_color: Literal["blue", "cyan", "green", "red", "yellow", "purple", "white"] = Field(default="cyan", description="Light strip accent color")

class SpaceDoorSchema(BaseModel):
    asset_type: Literal["space_door"] = "space_door"
    width: float = Field(default=150.0, ge=80.0, le=260.0, description="Space door width in centimeters")
    depth: float = Field(default=24.0, ge=8.0, le=60.0, description="Space door frame depth in centimeters")
    height: float = Field(default=240.0, ge=160.0, le=360.0, description="Space door height in centimeters")
    material: Literal["steel", "darksteel", "aluminum"] = Field(default="steel", description="Door frame material")
    accent_color: Literal["blue", "cyan", "green", "red", "yellow", "purple", "white"] = Field(default="cyan", description="Access panel light color")
    door_style: Literal["sliding", "iris"] = Field(default="sliding", description="Door opening style")

class AirlockSchema(BaseModel):
    asset_type: Literal["airlock"] = "airlock"
    width: float = Field(default=220.0, ge=120.0, le=360.0, description="Airlock chamber width in centimeters")
    depth: float = Field(default=280.0, ge=140.0, le=420.0, description="Airlock chamber depth in centimeters")
    height: float = Field(default=250.0, ge=160.0, le=360.0, description="Airlock chamber height in centimeters")
    material: Literal["steel", "darksteel", "aluminum"] = Field(default="steel", description="Airlock shell material")
    accent_color: Literal["blue", "cyan", "green", "red", "yellow", "purple", "white"] = Field(default="blue", description="Panel light color")
    door_count: int = Field(default=2, ge=1, le=2, description="Number of visible doors")
    has_control_panel: bool = Field(default=True, description="Whether the airlock includes a control panel")

class TurretSchema(BaseModel):
    asset_type: Literal["turret"] = "turret"
    width: float = Field(default=120.0, ge=50.0, le=220.0, description="Turret width in centimeters")
    depth: float = Field(default=140.0, ge=60.0, le=260.0, description="Turret depth in centimeters")
    height: float = Field(default=130.0, ge=50.0, le=220.0, description="Turret height in centimeters")
    material: Literal["steel", "darksteel", "aluminum"] = Field(default="darksteel", description="Turret shell material")
    accent_color: Literal["blue", "cyan", "green", "red", "yellow", "purple", "white"] = Field(default="red", description="Sensor light color")
    barrel_count: int = Field(default=2, ge=1, le=4, description="Number of weapon barrels")

class DroneSchema(BaseModel):
    asset_type: Literal["drone"] = "drone"
    width: float = Field(default=90.0, ge=30.0, le=180.0, description="Drone width in centimeters")
    depth: float = Field(default=90.0, ge=30.0, le=180.0, description="Drone depth in centimeters")
    height: float = Field(default=36.0, ge=12.0, le=90.0, description="Drone height in centimeters")
    material: Literal["plastic_dark", "plastic_white", "aluminum"] = Field(default="plastic_dark", description="Drone body material")
    accent_color: Literal["blue", "cyan", "green", "red", "yellow", "purple", "white"] = Field(default="cyan", description="Sensor light color")
    drone_style: Literal["quad", "hex"] = Field(default="quad", description="Rotor layout style")

class PipeSchema(BaseModel):
    asset_type: Literal["pipe"] = "pipe"
    diameter: float = Field(default=30.0, ge=8.0, le=90.0, description="Pipe diameter in centimeters")
    length: float = Field(default=220.0, ge=40.0, le=600.0, description="Pipe length in centimeters")
    material: Literal["steel", "iron", "aluminum"] = Field(default="steel", description="Pipe material")
    pipe_style: Literal["straight", "elbow"] = Field(default="straight", description="Pipe segment style")

class ValveSchema(BaseModel):
    asset_type: Literal["valve"] = "valve"
    diameter: float = Field(default=36.0, ge=12.0, le=80.0, description="Valve wheel/body diameter in centimeters")
    depth: float = Field(default=26.0, ge=8.0, le=60.0, description="Valve body depth in centimeters")
    material: Literal["steel", "iron", "aluminum"] = Field(default="steel", description="Valve body material")
    handle_style: Literal["wheel", "lever"] = Field(default="wheel", description="Valve handle style")

class TankSchema(BaseModel):
    asset_type: Literal["tank"] = "tank"
    diameter: float = Field(default=160.0, ge=60.0, le=360.0, description="Industrial tank diameter in centimeters")
    height: float = Field(default=260.0, ge=120.0, le=600.0, description="Industrial tank height or length in centimeters")
    material: Literal["steel", "iron", "aluminum"] = Field(default="steel", description="Tank shell material")
    orientation: Literal["vertical", "horizontal"] = Field(default="vertical", description="Tank mounting orientation")

class GeneratorSchema(BaseModel):
    asset_type: Literal["generator"] = "generator"
    width: float = Field(default=180.0, ge=80.0, le=320.0, description="Generator width in centimeters")
    depth: float = Field(default=120.0, ge=50.0, le=240.0, description="Generator depth in centimeters")
    height: float = Field(default=140.0, ge=60.0, le=240.0, description="Generator height in centimeters")
    material: Literal["steel", "darksteel", "aluminum"] = Field(default="darksteel", description="Generator housing material")
    accent_color: Literal["blue", "cyan", "green", "red", "yellow", "purple", "white"] = Field(default="yellow", description="Indicator or coil accent color")

class ConveyorBeltSchema(BaseModel):
    asset_type: Literal["conveyor_belt"] = "conveyor_belt"
    width: float = Field(default=90.0, ge=40.0, le=180.0, description="Conveyor width in centimeters")
    length: float = Field(default=320.0, ge=120.0, le=900.0, description="Conveyor length in centimeters")
    height: float = Field(default=90.0, ge=40.0, le=180.0, description="Conveyor working height in centimeters")
    material: Literal["steel", "darksteel", "aluminum"] = Field(default="steel", description="Frame material")
    roller_count: int = Field(default=6, ge=3, le=12, description="Number of visible rollers")

class ToolboxSchema(BaseModel):
    asset_type: Literal["toolbox"] = "toolbox"
    width: float = Field(default=62.0, ge=24.0, le=140.0, description="Toolbox width in centimeters")
    depth: float = Field(default=34.0, ge=14.0, le=70.0, description="Toolbox depth in centimeters")
    height: float = Field(default=34.0, ge=14.0, le=70.0, description="Toolbox height in centimeters")
    material: Literal["steel", "aluminum"] = Field(default="steel", description="Toolbox body material")
    has_tray: bool = Field(default=True, description="Whether the toolbox includes an inner tray")

class ForkliftSchema(BaseModel):
    asset_type: Literal["forklift"] = "forklift"
    width: float = Field(default=120.0, ge=70.0, le=220.0, description="Forklift width in centimeters")
    depth: float = Field(default=260.0, ge=120.0, le=520.0, description="Forklift length in centimeters")
    height: float = Field(default=220.0, ge=120.0, le=360.0, description="Forklift height in centimeters")
    material: Literal["hazard_yellow", "safety_orange", "steel"] = Field(default="hazard_yellow", description="Forklift primary body finish")
    has_load: bool = Field(default=False, description="Whether a pallet or box load is included")

class StorageRackSchema(BaseModel):
    asset_type: Literal["storage_rack"] = "storage_rack"
    width: float = Field(default=180.0, ge=80.0, le=340.0, description="Storage rack width in centimeters")
    depth: float = Field(default=60.0, ge=30.0, le=120.0, description="Storage rack depth in centimeters")
    height: float = Field(default=240.0, ge=120.0, le=360.0, description="Storage rack height in centimeters")
    material: Literal["steel", "aluminum"] = Field(default="steel", description="Rack frame material")
    shelves: int = Field(default=4, ge=2, le=8, description="Number of shelves")

class StreetLampSchema(BaseModel):
    asset_type: Literal["street_lamp"] = "street_lamp"
    width: float = Field(default=26.0, ge=10.0, le=60.0, description="Street lamp pole width in centimeters")
    depth: float = Field(default=30.0, ge=10.0, le=70.0, description="Street lamp head depth in centimeters")
    height: float = Field(default=340.0, ge=180.0, le=520.0, description="Street lamp height in centimeters")
    material: Literal["darksteel", "steel", "aluminum"] = Field(default="darksteel", description="Street lamp material")

class TrafficLightSchema(BaseModel):
    asset_type: Literal["traffic_light"] = "traffic_light"
    width: float = Field(default=46.0, ge=18.0, le=100.0, description="Traffic light housing width in centimeters")
    depth: float = Field(default=36.0, ge=14.0, le=80.0, description="Traffic light housing depth in centimeters")
    height: float = Field(default=320.0, ge=180.0, le=520.0, description="Traffic light overall height in centimeters")
    material: Literal["darksteel", "steel", "aluminum"] = Field(default="darksteel", description="Traffic light pole material")
    active_light: Literal["red", "yellow", "green"] = Field(default="green", description="Lit signal color")
    orientation: Literal["vertical", "horizontal"] = Field(default="vertical", description="Signal head orientation")

class RoadSignSchema(BaseModel):
    asset_type: Literal["road_sign"] = "road_sign"
    width: float = Field(default=70.0, ge=24.0, le=180.0, description="Road sign panel width in centimeters")
    depth: float = Field(default=10.0, ge=4.0, le=30.0, description="Road sign panel depth in centimeters")
    height: float = Field(default=260.0, ge=120.0, le=420.0, description="Road sign pole height in centimeters")
    material: Literal["aluminum", "steel"] = Field(default="aluminum", description="Road sign panel material")
    sign_shape: Literal["rectangle", "circle", "triangle"] = Field(default="rectangle", description="Road sign face shape")
    accent_color: Literal["white", "red", "blue", "yellow", "green"] = Field(default="white", description="Panel face color")

class StreetBenchSchema(BaseModel):
    asset_type: Literal["street_bench"] = "street_bench"
    width: float = Field(default=140.0, ge=80.0, le=240.0, description="Street bench width in centimeters")
    depth: float = Field(default=52.0, ge=30.0, le=100.0, description="Street bench depth in centimeters")
    height: float = Field(default=88.0, ge=40.0, le=140.0, description="Street bench total height in centimeters")
    material: Literal["darksteel", "steel", "concrete"] = Field(default="darksteel", description="Bench frame material")
    has_backrest: bool = Field(default=True, description="Whether the bench includes a backrest")

class MailboxSchema(BaseModel):
    asset_type: Literal["mailbox"] = "mailbox"
    width: float = Field(default=42.0, ge=18.0, le=90.0, description="Mailbox width in centimeters")
    depth: float = Field(default=62.0, ge=18.0, le=120.0, description="Mailbox depth in centimeters")
    height: float = Field(default=150.0, ge=70.0, le=260.0, description="Mailbox total height in centimeters")
    material: Literal["mail_red", "steel", "darksteel"] = Field(default="mail_red", description="Mailbox body material")
    mailbox_style: Literal["post", "wall"] = Field(default="post", description="Mailbox mounting style")

class TrashCanSchema(BaseModel):
    asset_type: Literal["trash_can"] = "trash_can"
    diameter: float = Field(default=48.0, ge=18.0, le=120.0, description="Trash can diameter in centimeters")
    height: float = Field(default=82.0, ge=30.0, le=160.0, description="Trash can height in centimeters")
    material: Literal["city_green", "steel", "darksteel"] = Field(default="city_green", description="Trash can body material")
    has_lid: bool = Field(default=True, description="Whether the trash can includes a lid")

class BusStopSchema(BaseModel):
    asset_type: Literal["bus_stop"] = "bus_stop"
    width: float = Field(default=280.0, ge=140.0, le=520.0, description="Bus stop shelter width in centimeters")
    depth: float = Field(default=120.0, ge=60.0, le=220.0, description="Bus stop shelter depth in centimeters")
    height: float = Field(default=240.0, ge=140.0, le=360.0, description="Bus stop shelter height in centimeters")
    material: Literal["steel", "darksteel", "aluminum"] = Field(default="steel", description="Bus stop frame material")
    has_bench: bool = Field(default=True, description="Whether the shelter includes a bench")

class PhoneBoothSchema(BaseModel):
    asset_type: Literal["phone_booth"] = "phone_booth"
    width: float = Field(default=120.0, ge=60.0, le=220.0, description="Phone booth width in centimeters")
    depth: float = Field(default=120.0, ge=60.0, le=220.0, description="Phone booth depth in centimeters")
    height: float = Field(default=240.0, ge=140.0, le=360.0, description="Phone booth height in centimeters")
    material: Literal["mail_red", "steel", "darksteel"] = Field(default="mail_red", description="Booth frame material")
    booth_style: Literal["classic", "enclosed"] = Field(default="classic", description="Phone booth enclosure style")
    accent_color: Literal["white", "blue", "yellow"] = Field(default="white", description="Sign or panel accent color")

class CarSchema(BaseModel):
    asset_type: Literal["car"] = "car"
    width: float = Field(default=180.0, ge=120.0, le=240.0, description="Car width in centimeters")
    depth: float = Field(default=420.0, ge=260.0, le=560.0, description="Car length in centimeters")
    height: float = Field(default=155.0, ge=110.0, le=220.0, description="Car height in centimeters")
    body_style: Literal["sedan", "hatchback", "suv"] = Field(default="sedan", description="Car body style")
    body_color: Literal["red", "blue", "green", "yellow", "white", "black", "silver", "gray", "orange"] = Field(default="red", description="Primary car body color")

class TruckSchema(BaseModel):
    asset_type: Literal["truck"] = "truck"
    width: float = Field(default=240.0, ge=160.0, le=320.0, description="Truck width in centimeters")
    depth: float = Field(default=620.0, ge=360.0, le=1000.0, description="Truck length in centimeters")
    height: float = Field(default=260.0, ge=160.0, le=420.0, description="Truck height in centimeters")
    truck_style: Literal["pickup", "box", "semi"] = Field(default="pickup", description="Truck body style")
    body_color: Literal["red", "blue", "green", "yellow", "white", "black", "silver", "gray", "orange"] = Field(default="blue", description="Primary truck body color")
    has_cargo: bool = Field(default=False, description="Whether the truck carries cargo")

class BikeSchema(BaseModel):
    asset_type: Literal["bike"] = "bike"
    width: float = Field(default=60.0, ge=30.0, le=90.0, description="Bike width in centimeters")
    depth: float = Field(default=180.0, ge=100.0, le=240.0, description="Bike length in centimeters")
    height: float = Field(default=115.0, ge=70.0, le=160.0, description="Bike height in centimeters")
    bike_style: Literal["road", "mountain", "city"] = Field(default="road", description="Bicycle style")
    frame_color: Literal["red", "blue", "green", "yellow", "white", "black", "silver", "orange"] = Field(default="green", description="Bike frame color")
    has_basket: bool = Field(default=False, description="Whether the bike includes a front basket")

class MotorcycleSchema(BaseModel):
    asset_type: Literal["motorcycle"] = "motorcycle"
    width: float = Field(default=80.0, ge=40.0, le=120.0, description="Motorcycle width in centimeters")
    depth: float = Field(default=220.0, ge=120.0, le=320.0, description="Motorcycle length in centimeters")
    height: float = Field(default=130.0, ge=70.0, le=190.0, description="Motorcycle height in centimeters")
    motorcycle_style: Literal["sport", "cruiser", "dirt"] = Field(default="sport", description="Motorcycle silhouette style")
    body_color: Literal["red", "blue", "green", "yellow", "white", "black", "silver", "gray", "orange"] = Field(default="orange", description="Motorcycle body color")
    has_windshield: bool = Field(default=True, description="Whether the motorcycle has a windshield or fairing screen")

class TractorSchema(BaseModel):
    asset_type: Literal["tractor"] = "tractor"
    width: float = Field(default=180.0, ge=110.0, le=260.0, description="Tractor width in centimeters")
    depth: float = Field(default=360.0, ge=220.0, le=520.0, description="Tractor length in centimeters")
    height: float = Field(default=240.0, ge=140.0, le=360.0, description="Tractor height in centimeters")
    body_color: Literal["red", "blue", "green", "yellow", "black", "gray", "orange"] = Field(default="green", description="Tractor body color")
    has_cab: bool = Field(default=True, description="Whether the tractor includes an enclosed cab")

class BattleTankSchema(BaseModel):
    asset_type: Literal["battle_tank"] = "battle_tank"
    width: float = Field(default=320.0, ge=180.0, le=460.0, description="Battle tank width in centimeters")
    depth: float = Field(default=640.0, ge=360.0, le=900.0, description="Battle tank length in centimeters")
    height: float = Field(default=220.0, ge=120.0, le=320.0, description="Battle tank height in centimeters")
    body_color: Literal["olive", "sand", "gray", "black"] = Field(default="olive", description="Battle tank camouflage color")
    turret_style: Literal["angular", "rounded"] = Field(default="angular", description="Turret silhouette style")

class BoatSchema(BaseModel):
    asset_type: Literal["boat"] = "boat"
    width: float = Field(default=180.0, ge=80.0, le=320.0, description="Boat width in centimeters")
    depth: float = Field(default=460.0, ge=180.0, le=900.0, description="Boat length in centimeters")
    height: float = Field(default=160.0, ge=60.0, le=320.0, description="Boat height in centimeters")
    boat_style: Literal["motorboat", "rowboat", "sailboat"] = Field(default="motorboat", description="Boat type")
    hull_material: Literal["wood", "steel", "fiberglass"] = Field(default="fiberglass", description="Boat hull material")
    has_canopy: bool = Field(default=False, description="Whether the boat includes a canopy")

class CanoeSchema(BaseModel):
    asset_type: Literal["canoe"] = "canoe"
    width: float = Field(default=90.0, ge=40.0, le=160.0, description="Canoe width in centimeters")
    depth: float = Field(default=420.0, ge=180.0, le=700.0, description="Canoe length in centimeters")
    height: float = Field(default=90.0, ge=30.0, le=160.0, description="Canoe height in centimeters")
    material: Literal["wood", "fiberglass"] = Field(default="wood", description="Canoe hull material")
    seat_count: int = Field(default=2, ge=1, le=3, description="Number of seats")

class ShipSchema(BaseModel):
    asset_type: Literal["ship"] = "ship"
    width: float = Field(default=320.0, ge=160.0, le=700.0, description="Ship width in centimeters")
    depth: float = Field(default=1200.0, ge=500.0, le=2200.0, description="Ship length in centimeters")
    height: float = Field(default=340.0, ge=160.0, le=700.0, description="Ship height in centimeters")
    ship_style: Literal["cargo", "sailing", "warship"] = Field(default="cargo", description="Ship category")
    hull_material: Literal["steel", "wood"] = Field(default="steel", description="Ship hull material")

class PlaneSchema(BaseModel):
    asset_type: Literal["plane"] = "plane"
    width: float = Field(default=1200.0, ge=400.0, le=2200.0, description="Plane wingspan width in centimeters")
    depth: float = Field(default=900.0, ge=400.0, le=1800.0, description="Plane length in centimeters")
    height: float = Field(default=260.0, ge=120.0, le=500.0, description="Plane height in centimeters")
    plane_style: Literal["prop", "jet"] = Field(default="jet", description="Aircraft propulsion style")
    body_color: Literal["white", "silver", "blue", "red", "gray"] = Field(default="white", description="Plane body color")

class HelicopterSchema(BaseModel):
    asset_type: Literal["helicopter"] = "helicopter"
    width: float = Field(default=320.0, ge=140.0, le=700.0, description="Helicopter body width in centimeters")
    depth: float = Field(default=820.0, ge=300.0, le=1600.0, description="Helicopter body length in centimeters")
    height: float = Field(default=300.0, ge=140.0, le=560.0, description="Helicopter height in centimeters")
    body_color: Literal["red", "blue", "green", "white", "black", "gray", "yellow"] = Field(default="gray", description="Helicopter body color")
    has_skids: bool = Field(default=True, description="Whether the helicopter has skids")

class MaleSchema(BaseModel):
    asset_type: Literal["male"] = "male"
    width: float = Field(default=58.0, ge=30.0, le=90.0, description="Male character shoulder width in centimeters")
    depth: float = Field(default=40.0, ge=20.0, le=70.0, description="Male character depth in centimeters")
    height: float = Field(default=178.0, ge=120.0, le=220.0, description="Male character height in centimeters")
    skin_tone: Literal["light", "medium", "dark"] = Field(default="medium", description="Skin tone")
    outfit_color: Literal["red", "blue", "green", "brown", "black", "white", "gray"] = Field(default="blue", description="Outfit color")

class FemaleSchema(BaseModel):
    asset_type: Literal["female"] = "female"
    width: float = Field(default=54.0, ge=28.0, le=85.0, description="Female character shoulder width in centimeters")
    depth: float = Field(default=36.0, ge=18.0, le=65.0, description="Female character depth in centimeters")
    height: float = Field(default=168.0, ge=110.0, le=210.0, description="Female character height in centimeters")
    skin_tone: Literal["light", "medium", "dark"] = Field(default="light", description="Skin tone")
    outfit_color: Literal["red", "blue", "green", "brown", "black", "white", "gray"] = Field(default="red", description="Outfit color")

class ChildSchema(BaseModel):
    asset_type: Literal["child"] = "child"
    width: float = Field(default=42.0, ge=20.0, le=70.0, description="Child character width in centimeters")
    depth: float = Field(default=28.0, ge=14.0, le=50.0, description="Child character depth in centimeters")
    height: float = Field(default=118.0, ge=70.0, le=150.0, description="Child character height in centimeters")
    skin_tone: Literal["light", "medium", "dark"] = Field(default="light", description="Skin tone")
    outfit_color: Literal["red", "blue", "green", "brown", "black", "white", "gray"] = Field(default="green", description="Outfit color")

class ElderSchema(BaseModel):
    asset_type: Literal["elder"] = "elder"
    width: float = Field(default=56.0, ge=28.0, le=90.0, description="Elder character width in centimeters")
    depth: float = Field(default=38.0, ge=18.0, le=65.0, description="Elder character depth in centimeters")
    height: float = Field(default=166.0, ge=100.0, le=210.0, description="Elder character height in centimeters")
    skin_tone: Literal["light", "medium", "dark"] = Field(default="light", description="Skin tone")
    outfit_color: Literal["red", "blue", "green", "brown", "black", "white", "gray"] = Field(default="brown", description="Outfit color")

class MerchantSchema(BaseModel):
    asset_type: Literal["merchant"] = "merchant"
    width: float = Field(default=58.0, ge=30.0, le=90.0, description="Merchant character width in centimeters")
    depth: float = Field(default=40.0, ge=20.0, le=70.0, description="Merchant character depth in centimeters")
    height: float = Field(default=176.0, ge=120.0, le=220.0, description="Merchant character height in centimeters")
    skin_tone: Literal["light", "medium", "dark"] = Field(default="medium", description="Skin tone")
    outfit_color: Literal["red", "blue", "green", "brown", "black", "white", "gray"] = Field(default="green", description="Outfit color")

class GuardSchema(BaseModel):
    asset_type: Literal["guard"] = "guard"
    width: float = Field(default=62.0, ge=30.0, le=95.0, description="Guard character width in centimeters")
    depth: float = Field(default=42.0, ge=20.0, le=72.0, description="Guard character depth in centimeters")
    height: float = Field(default=184.0, ge=120.0, le=230.0, description="Guard character height in centimeters")
    skin_tone: Literal["light", "medium", "dark"] = Field(default="medium", description="Skin tone")
    outfit_color: Literal["red", "blue", "green", "brown", "black", "white", "gray"] = Field(default="blue", description="Uniform color")

class FarmerSchema(BaseModel):
    asset_type: Literal["farmer"] = "farmer"
    width: float = Field(default=58.0, ge=30.0, le=90.0, description="Farmer character width in centimeters")
    depth: float = Field(default=40.0, ge=20.0, le=70.0, description="Farmer character depth in centimeters")
    height: float = Field(default=172.0, ge=120.0, le=220.0, description="Farmer character height in centimeters")
    skin_tone: Literal["light", "medium", "dark"] = Field(default="medium", description="Skin tone")
    outfit_color: Literal["red", "blue", "green", "brown", "black", "white", "gray"] = Field(default="brown", description="Workwear color")

class BlacksmithSchema(BaseModel):
    asset_type: Literal["blacksmith"] = "blacksmith"
    width: float = Field(default=64.0, ge=34.0, le=100.0, description="Blacksmith character width in centimeters")
    depth: float = Field(default=42.0, ge=22.0, le=72.0, description="Blacksmith character depth in centimeters")
    height: float = Field(default=176.0, ge=120.0, le=220.0, description="Blacksmith character height in centimeters")
    skin_tone: Literal["light", "medium", "dark"] = Field(default="medium", description="Skin tone")
    outfit_color: Literal["red", "blue", "green", "brown", "black", "white", "gray"] = Field(default="brown", description="Apron or clothing color")

class SoldierSchema(BaseModel):
    asset_type: Literal["soldier"] = "soldier"
    width: float = Field(default=62.0, ge=32.0, le=96.0, description="Soldier character width in centimeters")
    depth: float = Field(default=42.0, ge=20.0, le=72.0, description="Soldier character depth in centimeters")
    height: float = Field(default=182.0, ge=120.0, le=230.0, description="Soldier character height in centimeters")
    skin_tone: Literal["light", "medium", "dark"] = Field(default="medium", description="Skin tone")
    outfit_color: Literal["red", "blue", "green", "brown", "black", "white", "gray"] = Field(default="red", description="Uniform color")

class ElfSchema(BaseModel):
    asset_type: Literal["elf"] = "elf"
    width: float = Field(default=54.0, ge=28.0, le=86.0, description="Elf character width in centimeters")
    depth: float = Field(default=36.0, ge=18.0, le=64.0, description="Elf character depth in centimeters")
    height: float = Field(default=186.0, ge=130.0, le=240.0, description="Elf character height in centimeters")
    skin_tone: Literal["light", "medium", "dark"] = Field(default="light", description="Skin tone")
    outfit_color: Literal["red", "blue", "green", "brown", "black", "white", "gray"] = Field(default="green", description="Outfit color")

class OrcSchema(BaseModel):
    asset_type: Literal["orc"] = "orc"
    width: float = Field(default=72.0, ge=36.0, le=110.0, description="Orc character width in centimeters")
    depth: float = Field(default=48.0, ge=24.0, le=80.0, description="Orc character depth in centimeters")
    height: float = Field(default=198.0, ge=130.0, le=260.0, description="Orc character height in centimeters")
    skin_tone: Literal["light", "medium", "dark"] = Field(default="medium", description="Skin tone")
    outfit_color: Literal["red", "blue", "green", "brown", "black", "white", "gray"] = Field(default="brown", description="Armor or cloth color")

class GoblinSchema(BaseModel):
    asset_type: Literal["goblin"] = "goblin"
    width: float = Field(default=42.0, ge=20.0, le=68.0, description="Goblin character width in centimeters")
    depth: float = Field(default=28.0, ge=12.0, le=48.0, description="Goblin character depth in centimeters")
    height: float = Field(default=112.0, ge=70.0, le=150.0, description="Goblin character height in centimeters")
    skin_tone: Literal["light", "medium", "dark"] = Field(default="medium", description="Skin tone")
    outfit_color: Literal["red", "blue", "green", "brown", "black", "white", "gray"] = Field(default="brown", description="Clothing color")

class DwarfSchema(BaseModel):
    asset_type: Literal["dwarf"] = "dwarf"
    width: float = Field(default=64.0, ge=32.0, le=96.0, description="Dwarf character width in centimeters")
    depth: float = Field(default=42.0, ge=20.0, le=72.0, description="Dwarf character depth in centimeters")
    height: float = Field(default=132.0, ge=80.0, le=180.0, description="Dwarf character height in centimeters")
    skin_tone: Literal["light", "medium", "dark"] = Field(default="light", description="Skin tone")
    outfit_color: Literal["red", "blue", "green", "brown", "black", "white", "gray"] = Field(default="blue", description="Clothing or armor color")

class DragonSchema(BaseModel):
    asset_type: Literal["dragon"] = "dragon"
    width: float = Field(default=260.0, ge=120.0, le=520.0, description="Dragon wingspan/body width in centimeters")
    depth: float = Field(default=520.0, ge=220.0, le=1200.0, description="Dragon body length in centimeters")
    height: float = Field(default=240.0, ge=120.0, le=520.0, description="Dragon height in centimeters")
    scale_color: Literal["red", "green", "blue", "black", "gray", "brown"] = Field(default="green", description="Primary scale color")
    pose: Literal["standing", "flying", "perched"] = Field(default="standing", description="Dragon pose")

class DogSchema(BaseModel):
    asset_type: Literal["dog"] = "dog"
    width: float = Field(default=46.0, ge=20.0, le=90.0, description="Dog width in centimeters")
    depth: float = Field(default=90.0, ge=40.0, le=160.0, description="Dog body length in centimeters")
    height: float = Field(default=62.0, ge=24.0, le=110.0, description="Dog height in centimeters")
    fur_color: Literal["brown", "black", "white", "golden", "gray", "orange", "tan"] = Field(default="brown", description="Primary fur color")

class CatSchema(BaseModel):
    asset_type: Literal["cat"] = "cat"
    width: float = Field(default=30.0, ge=14.0, le=60.0, description="Cat width in centimeters")
    depth: float = Field(default=54.0, ge=24.0, le=100.0, description="Cat body length in centimeters")
    height: float = Field(default=36.0, ge=16.0, le=64.0, description="Cat height in centimeters")
    fur_color: Literal["brown", "black", "white", "golden", "gray", "orange", "tan"] = Field(default="orange", description="Primary fur color")

class HorseSchema(BaseModel):
    asset_type: Literal["horse"] = "horse"
    width: float = Field(default=80.0, ge=40.0, le=140.0, description="Horse width in centimeters")
    depth: float = Field(default=180.0, ge=80.0, le=300.0, description="Horse body length in centimeters")
    height: float = Field(default=160.0, ge=80.0, le=240.0, description="Horse height in centimeters")
    fur_color: Literal["brown", "black", "white", "gray", "tan"] = Field(default="brown", description="Coat color")

class CowSchema(BaseModel):
    asset_type: Literal["cow"] = "cow"
    width: float = Field(default=84.0, ge=40.0, le=150.0, description="Cow width in centimeters")
    depth: float = Field(default=170.0, ge=80.0, le=320.0, description="Cow body length in centimeters")
    height: float = Field(default=138.0, ge=70.0, le=220.0, description="Cow height in centimeters")
    fur_color: Literal["brown", "black", "white", "gray", "tan"] = Field(default="white", description="Coat color")

class DeerSchema(BaseModel):
    asset_type: Literal["deer"] = "deer"
    width: float = Field(default=66.0, ge=30.0, le=120.0, description="Deer width in centimeters")
    depth: float = Field(default=132.0, ge=60.0, le=240.0, description="Deer body length in centimeters")
    height: float = Field(default=122.0, ge=60.0, le=220.0, description="Deer height in centimeters")
    fur_color: Literal["brown", "black", "white", "gray", "tan"] = Field(default="tan", description="Coat color")

class WolfSchema(BaseModel):
    asset_type: Literal["wolf"] = "wolf"
    width: float = Field(default=50.0, ge=24.0, le=96.0, description="Wolf width in centimeters")
    depth: float = Field(default=110.0, ge=50.0, le=180.0, description="Wolf body length in centimeters")
    height: float = Field(default=72.0, ge=30.0, le=120.0, description="Wolf height in centimeters")
    fur_color: Literal["brown", "black", "white", "gray", "tan"] = Field(default="gray", description="Coat color")

class BirdSchema(BaseModel):
    asset_type: Literal["bird"] = "bird"
    width: float = Field(default=42.0, ge=14.0, le=120.0, description="Bird wingspan or body width in centimeters")
    depth: float = Field(default=60.0, ge=14.0, le=140.0, description="Bird body length in centimeters")
    height: float = Field(default=46.0, ge=10.0, le=120.0, description="Bird height in centimeters")
    body_color: Literal["red", "blue", "green", "yellow", "white", "black", "gray", "orange"] = Field(default="blue", description="Feather color")
    bird_style: Literal["perched", "flying", "songbird"] = Field(default="perched", description="Bird pose/style")

class FishSchema(BaseModel):
    asset_type: Literal["fish"] = "fish"
    width: float = Field(default=24.0, ge=8.0, le=120.0, description="Fish body width in centimeters")
    depth: float = Field(default=72.0, ge=14.0, le=220.0, description="Fish body length in centimeters")
    height: float = Field(default=26.0, ge=6.0, le=100.0, description="Fish body height in centimeters")
    body_color: Literal["red", "blue", "green", "yellow", "white", "black", "gray", "orange", "silver"] = Field(default="silver", description="Fish body color")
    fish_style: Literal["stream", "tropical", "shark"] = Field(default="stream", description="Fish category")

class CoinSchema(BaseModel):
    asset_type: Literal["coin"] = "coin"
    width: float = Field(default=4.0, ge=1.0, le=12.0, description="Coin diameter width in centimeters")
    depth: float = Field(default=4.0, ge=1.0, le=12.0, description="Coin diameter depth in centimeters")
    height: float = Field(default=0.4, ge=0.1, le=2.0, description="Coin thickness in centimeters")

class GemSchema(BaseModel):
    asset_type: Literal["gem"] = "gem"
    width: float = Field(default=12.0, ge=3.0, le=40.0, description="Gem width in centimeters")
    depth: float = Field(default=12.0, ge=3.0, le=40.0, description="Gem depth in centimeters")
    height: float = Field(default=18.0, ge=4.0, le=50.0, description="Gem height in centimeters")
    gem_color: Literal["red", "blue", "green", "yellow", "purple", "white"] = Field(default="purple", description="Gem color")

class KeySchema(BaseModel):
    asset_type: Literal["key"] = "key"
    width: float = Field(default=4.0, ge=1.0, le=14.0, description="Key ring width in centimeters")
    depth: float = Field(default=16.0, ge=4.0, le=40.0, description="Key length in centimeters")
    height: float = Field(default=2.0, ge=0.5, le=6.0, description="Key thickness in centimeters")
    material: Literal["gold", "bronze", "steel"] = Field(default="gold", description="Key material")

class ScrollSchema(BaseModel):
    asset_type: Literal["scroll"] = "scroll"
    width: float = Field(default=16.0, ge=6.0, le=40.0, description="Scroll width in centimeters")
    depth: float = Field(default=34.0, ge=10.0, le=70.0, description="Scroll length in centimeters")
    height: float = Field(default=6.0, ge=1.0, le=20.0, description="Scroll roll thickness in centimeters")
    tied: bool = Field(default=True, description="Whether the scroll is tied with a ribbon")

class PotionSchema(BaseModel):
    asset_type: Literal["potion"] = "potion"
    width: float = Field(default=12.0, ge=4.0, le=36.0, description="Potion bottle width in centimeters")
    depth: float = Field(default=12.0, ge=4.0, le=36.0, description="Potion bottle depth in centimeters")
    height: float = Field(default=28.0, ge=10.0, le=60.0, description="Potion bottle height in centimeters")
    liquid_color: Literal["red", "blue", "green"] = Field(default="blue", description="Potion liquid color")

class TreasureChestSchema(BaseModel):
    asset_type: Literal["treasure_chest"] = "treasure_chest"
    width: float = Field(default=90.0, ge=40.0, le=180.0, description="Treasure chest width in centimeters")
    depth: float = Field(default=56.0, ge=24.0, le=120.0, description="Treasure chest depth in centimeters")
    height: float = Field(default=62.0, ge=24.0, le=140.0, description="Treasure chest height in centimeters")
    material: Literal["wood", "darkwood", "steel"] = Field(default="wood", description="Treasure chest body material")
    has_gems: bool = Field(default=True, description="Whether the chest includes a top gem ornament")

class ArtifactSchema(BaseModel):
    asset_type: Literal["artifact"] = "artifact"
    width: float = Field(default=34.0, ge=12.0, le=90.0, description="Artifact width in centimeters")
    depth: float = Field(default=34.0, ge=12.0, le=90.0, description="Artifact depth in centimeters")
    height: float = Field(default=72.0, ge=20.0, le=160.0, description="Artifact height in centimeters")
    artifact_style: Literal["obelisk", "orb"] = Field(default="obelisk", description="Artifact silhouette style")

class TerrainSchema(BaseModel):
    asset_type: Literal["terrain"] = "terrain"
    width: float = Field(default=500.0, ge=180.0, le=1200.0, description="Terrain patch width in centimeters")
    depth: float = Field(default=500.0, ge=180.0, le=1200.0, description="Terrain patch depth in centimeters")
    height: float = Field(default=90.0, ge=20.0, le=260.0, description="Terrain elevation variation in centimeters")
    material: Literal["grass", "dirt", "stone"] = Field(default="grass", description="Surface material")

class HillSchema(BaseModel):
    asset_type: Literal["hill"] = "hill"
    width: float = Field(default=340.0, ge=140.0, le=900.0, description="Hill width in centimeters")
    depth: float = Field(default=340.0, ge=140.0, le=900.0, description="Hill depth in centimeters")
    height: float = Field(default=180.0, ge=60.0, le=520.0, description="Hill height in centimeters")

class MountainSchema(BaseModel):
    asset_type: Literal["mountain"] = "mountain"
    width: float = Field(default=420.0, ge=180.0, le=1200.0, description="Mountain base width in centimeters")
    depth: float = Field(default=420.0, ge=180.0, le=1200.0, description="Mountain base depth in centimeters")
    height: float = Field(default=520.0, ge=180.0, le=1800.0, description="Mountain height in centimeters")

class CliffSchema(BaseModel):
    asset_type: Literal["cliff"] = "cliff"
    width: float = Field(default=420.0, ge=180.0, le=1200.0, description="Cliff width in centimeters")
    depth: float = Field(default=180.0, ge=60.0, le=520.0, description="Cliff depth in centimeters")
    height: float = Field(default=320.0, ge=120.0, le=1200.0, description="Cliff height in centimeters")

class ValleySchema(BaseModel):
    asset_type: Literal["valley"] = "valley"
    width: float = Field(default=520.0, ge=200.0, le=1400.0, description="Valley width in centimeters")
    depth: float = Field(default=420.0, ge=180.0, le=1200.0, description="Valley depth in centimeters")
    height: float = Field(default=180.0, ge=60.0, le=520.0, description="Valley side-wall height in centimeters")

class CaveSchema(BaseModel):
    asset_type: Literal["cave"] = "cave"
    width: float = Field(default=320.0, ge=140.0, le=900.0, description="Cave width in centimeters")
    depth: float = Field(default=260.0, ge=120.0, le=700.0, description="Cave depth in centimeters")
    height: float = Field(default=220.0, ge=100.0, le=600.0, description="Cave height in centimeters")

class GroundTileSchema(BaseModel):
    asset_type: Literal["ground_tile"] = "ground_tile"
    width: float = Field(default=200.0, ge=80.0, le=400.0, description="Ground tile width in centimeters")
    depth: float = Field(default=200.0, ge=80.0, le=400.0, description="Ground tile depth in centimeters")
    height: float = Field(default=20.0, ge=4.0, le=60.0, description="Ground tile thickness in centimeters")

class RoadTileSchema(BaseModel):
    asset_type: Literal["road_tile"] = "road_tile"
    width: float = Field(default=220.0, ge=80.0, le=500.0, description="Road tile width in centimeters")
    depth: float = Field(default=220.0, ge=80.0, le=500.0, description="Road tile depth in centimeters")
    height: float = Field(default=18.0, ge=4.0, le=60.0, description="Road tile thickness in centimeters")

class PathTileSchema(BaseModel):
    asset_type: Literal["path_tile"] = "path_tile"
    width: float = Field(default=200.0, ge=80.0, le=400.0, description="Path tile width in centimeters")
    depth: float = Field(default=200.0, ge=80.0, le=400.0, description="Path tile depth in centimeters")
    height: float = Field(default=16.0, ge=4.0, le=60.0, description="Path tile thickness in centimeters")

class RiverTileSchema(BaseModel):
    asset_type: Literal["river_tile"] = "river_tile"
    width: float = Field(default=220.0, ge=80.0, le=500.0, description="River tile width in centimeters")
    depth: float = Field(default=220.0, ge=80.0, le=500.0, description="River tile depth in centimeters")
    height: float = Field(default=20.0, ge=4.0, le=60.0, description="River tile thickness in centimeters")

class DungeonTileSchema(BaseModel):
    asset_type: Literal["dungeon_tile"] = "dungeon_tile"
    width: float = Field(default=200.0, ge=80.0, le=400.0, description="Dungeon tile width in centimeters")
    depth: float = Field(default=200.0, ge=80.0, le=400.0, description="Dungeon tile depth in centimeters")
    height: float = Field(default=18.0, ge=4.0, le=60.0, description="Dungeon tile thickness in centimeters")

class GameBackground2DSchema(BaseModel):
    asset_type: Literal["game_background_2d"] = "game_background_2d"
    width: float = Field(default=1400.0, ge=500.0, le=3200.0, description="Background scene width in centimeters")
    depth: float = Field(default=36.0, ge=8.0, le=120.0, description="Parallax depth from front to back in centimeters")
    height: float = Field(default=800.0, ge=240.0, le=1800.0, description="Background scene height in centimeters")
    theme: Literal["forest", "desert", "city", "cave", "snow", "space", "volcanic"] = Field(default="forest", description="Overall background art theme")
    time_of_day: Literal["day", "sunset", "night", "dawn"] = Field(default="day", description="Lighting mood for the background")
    layer_count: int = Field(default=4, ge=3, le=7, description="Number of silhouette depth layers")
    has_celestial: bool = Field(default=True, description="Whether to include a sun, moon, or planet element")

AssetParams = Union[
    SwordSchema, DaggerSchema, HammerSchema, MaceSchema, SpearSchema, HalberdSchema, StaffSchema, BowSchema,
    CrossbowSchema, ArrowSchema, BoltSchema, MagicStaffSchema, WandSchema, OrbSchema,
    TableSchema, DiningTableSchema, CoffeeTableSchema, BarrelSchema, CrateSchema, ShieldSchema, 
    ChairSchema, DeskSchema, StoolSchema, ChestSchema, AxeSchema, HelmetSchema, TorchSchema, SofaSchema, 
    BenchSchema, CouchSchema, ArmchairSchema, BedSchema, BunkBedSchema, WardrobeSchema, StorageSchema, 
    LightingSchema, ClosetSchema, DresserSchema, CabinetSchema, ShelfSchema, BookcaseSchema, NightstandSchema, TVStandSchema,
    FridgeSchema, StoveSchema, OvenSchema, MicrowaveSchema, SinkSchema, CountertopSchema,
    CupboardSchema, KitchenIslandSchema, DiningSetSchema, ToiletSchema, BathtubSchema, ShowerSchema,
    MirrorSchema, TowelRackSchema, LampSchema, ChandelierSchema, PaintingSchema, PictureFrameSchema,
    ClockSchema, VaseSchema, PlantPotSchema, RugSchema,
    WallSchema, FloorSchema, CeilingSchema, RoofSchema, PillarSchema, BeamSchema,
    FoundationSchema, DoorSchema, WindowSchema, ArchwaySchema, GateSchema, StairsSchema, LadderSchema,
    RampSchema, BridgeSchema, BalconySchema, FenceSchema, RailingSchema, ChimneySchema, PorchSchema,
    OakTreeSchema, PineTreeSchema, BirchTreeSchema, PalmTreeSchema, DeadTreeSchema, SaplingSchema,
    GrassSchema, BushSchema, ShrubSchema, FernSchema, FlowerSchema, MossSchema,
    SmallRockSchema, BoulderSchema, RockClusterSchema, CliffSectionSchema,
    LogSchema, TreeStumpSchema, FallenTreeSchema, MushroomSchema, VineSchema, RootSchema,
    PondSchema, RiverSegmentSchema, WaterfallSchema, StreamSchema,
    ChestplateSchema, GauntletsSchema, BootsSchema, BackpackSchema, BeltSchema, PouchSchema, CapeSchema,
    TentSchema, CampfireSchema, SleepingBagSchema, LanternSchema, CookingPotSchema, SupplyBoxSchema,
    CastleWallSchema, TowerSchema, DrawbridgeSchema, ThroneSchema, BannerSchema, MarketStallSchema,
    WellSchema, CartSchema, AnvilSchema, ForgeSchema,
    ControlPanelSchema, TerminalSchema, ComputerSchema, ServerRackSchema, EnergyCellSchema, TechCrateSchema,
    SpaceDoorSchema, AirlockSchema, TurretSchema, DroneSchema, PipeSchema, ValveSchema, TankSchema,
    GeneratorSchema, ConveyorBeltSchema, ToolboxSchema, ForkliftSchema, StorageRackSchema,
    StreetLampSchema, TrafficLightSchema, RoadSignSchema, StreetBenchSchema, MailboxSchema,
    TrashCanSchema, BusStopSchema, PhoneBoothSchema,
    CarSchema, TruckSchema, BikeSchema, MotorcycleSchema, TractorSchema, BattleTankSchema,
    BoatSchema, CanoeSchema, ShipSchema, PlaneSchema, HelicopterSchema,
    MaleSchema, FemaleSchema, ChildSchema, ElderSchema, MerchantSchema, GuardSchema, FarmerSchema,
    BlacksmithSchema, SoldierSchema, ElfSchema, OrcSchema, GoblinSchema, DwarfSchema, DragonSchema,
    DogSchema, CatSchema, HorseSchema, CowSchema, DeerSchema, WolfSchema, BirdSchema, FishSchema,
    CoinSchema, GemSchema, KeySchema, ScrollSchema, PotionSchema, TreasureChestSchema, ArtifactSchema,
    TerrainSchema, HillSchema, MountainSchema, CliffSchema, ValleySchema, CaveSchema,
    GroundTileSchema, RoadTileSchema, PathTileSchema, RiverTileSchema, DungeonTileSchema, GameBackground2DSchema
]

SCHEMA_BY_ASSET_TYPE = {
    "sword": SwordSchema,
    "dagger": DaggerSchema,
    "hammer": HammerSchema,
    "mace": MaceSchema,
    "spear": SpearSchema,
    "halberd": HalberdSchema,
    "staff": StaffSchema,
    "bow": BowSchema,
    "crossbow": CrossbowSchema,
    "arrow": ArrowSchema,
    "bolt": BoltSchema,
    "magic_staff": MagicStaffSchema,
    "wand": WandSchema,
    "orb": OrbSchema,
    "table": TableSchema,
    "dining_table": DiningTableSchema,
    "coffee_table": CoffeeTableSchema,
    "barrel": BarrelSchema,
    "crate": CrateSchema,
    "shield": ShieldSchema,
    "chair": ChairSchema,
    "desk": DeskSchema,
    "stool": StoolSchema,
    "chest": ChestSchema,
    "axe": AxeSchema,
    "helmet": HelmetSchema,
    "torch": TorchSchema,
    "sofa": SofaSchema,
    "bench": BenchSchema,
    "couch": CouchSchema,
    "armchair": ArmchairSchema,
    "bed": BedSchema,
    "bunk_bed": BunkBedSchema,
    "wardrobe": WardrobeSchema,
    "storage": StorageSchema,
    "lighting": LightingSchema,
    "closet": ClosetSchema,
    "dresser": DresserSchema,
    "cabinet": CabinetSchema,
    "shelf": ShelfSchema,
    "bookcase": BookcaseSchema,
    "nightstand": NightstandSchema,
    "tv_stand": TVStandSchema,
    "fridge": FridgeSchema,
    "stove": StoveSchema,
    "oven": OvenSchema,
    "microwave": MicrowaveSchema,
    "sink": SinkSchema,
    "countertop": CountertopSchema,
    "cupboard": CupboardSchema,
    "kitchen_island": KitchenIslandSchema,
    "dining_set": DiningSetSchema,
    "toilet": ToiletSchema,
    "bathtub": BathtubSchema,
    "shower": ShowerSchema,
    "mirror": MirrorSchema,
    "towel_rack": TowelRackSchema,
    "lamp": LampSchema,
    "chandelier": ChandelierSchema,
    "painting": PaintingSchema,
    "picture_frame": PictureFrameSchema,
    "clock": ClockSchema,
    "vase": VaseSchema,
    "plant_pot": PlantPotSchema,
    "rug": RugSchema,
    "wall": WallSchema,
    "floor": FloorSchema,
    "ceiling": CeilingSchema,
    "roof": RoofSchema,
    "pillar": PillarSchema,
    "beam": BeamSchema,
    "foundation": FoundationSchema,
    "door": DoorSchema,
    "window": WindowSchema,
    "archway": ArchwaySchema,
    "gate": GateSchema,
    "stairs": StairsSchema,
    "ladder": LadderSchema,
    "ramp": RampSchema,
    "bridge": BridgeSchema,
    "balcony": BalconySchema,
    "fence": FenceSchema,
    "railing": RailingSchema,
    "chimney": ChimneySchema,
    "porch": PorchSchema,
    "oak_tree": OakTreeSchema,
    "pine_tree": PineTreeSchema,
    "birch_tree": BirchTreeSchema,
    "palm_tree": PalmTreeSchema,
    "dead_tree": DeadTreeSchema,
    "sapling": SaplingSchema,
    "grass": GrassSchema,
    "bush": BushSchema,
    "shrub": ShrubSchema,
    "fern": FernSchema,
    "flower": FlowerSchema,
    "moss": MossSchema,
    "small_rock": SmallRockSchema,
    "boulder": BoulderSchema,
    "rock_cluster": RockClusterSchema,
    "cliff_section": CliffSectionSchema,
    "log": LogSchema,
    "tree_stump": TreeStumpSchema,
    "fallen_tree": FallenTreeSchema,
    "mushroom": MushroomSchema,
    "vine": VineSchema,
    "root": RootSchema,
    "pond": PondSchema,
    "river_segment": RiverSegmentSchema,
    "waterfall": WaterfallSchema,
    "stream": StreamSchema,
    "chestplate": ChestplateSchema,
    "gauntlets": GauntletsSchema,
    "boots": BootsSchema,
    "backpack": BackpackSchema,
    "belt": BeltSchema,
    "pouch": PouchSchema,
    "cape": CapeSchema,
    "tent": TentSchema,
    "campfire": CampfireSchema,
    "sleeping_bag": SleepingBagSchema,
    "lantern": LanternSchema,
    "cooking_pot": CookingPotSchema,
    "supply_box": SupplyBoxSchema,
    "castle_wall": CastleWallSchema,
    "tower": TowerSchema,
    "drawbridge": DrawbridgeSchema,
    "throne": ThroneSchema,
    "banner": BannerSchema,
    "market_stall": MarketStallSchema,
    "well": WellSchema,
    "cart": CartSchema,
    "anvil": AnvilSchema,
    "forge": ForgeSchema,
    "control_panel": ControlPanelSchema,
    "terminal": TerminalSchema,
    "computer": ComputerSchema,
    "server_rack": ServerRackSchema,
    "energy_cell": EnergyCellSchema,
    "tech_crate": TechCrateSchema,
    "space_door": SpaceDoorSchema,
    "airlock": AirlockSchema,
    "turret": TurretSchema,
    "drone": DroneSchema,
    "pipe": PipeSchema,
    "valve": ValveSchema,
    "tank": TankSchema,
    "generator": GeneratorSchema,
    "conveyor_belt": ConveyorBeltSchema,
    "toolbox": ToolboxSchema,
    "forklift": ForkliftSchema,
    "storage_rack": StorageRackSchema,
    "street_lamp": StreetLampSchema,
    "traffic_light": TrafficLightSchema,
    "road_sign": RoadSignSchema,
    "street_bench": StreetBenchSchema,
    "mailbox": MailboxSchema,
    "trash_can": TrashCanSchema,
    "bus_stop": BusStopSchema,
    "phone_booth": PhoneBoothSchema,
    "car": CarSchema,
    "truck": TruckSchema,
    "bike": BikeSchema,
    "motorcycle": MotorcycleSchema,
    "tractor": TractorSchema,
    "battle_tank": BattleTankSchema,
    "boat": BoatSchema,
    "canoe": CanoeSchema,
    "ship": ShipSchema,
    "plane": PlaneSchema,
    "helicopter": HelicopterSchema,
    "male": MaleSchema,
    "female": FemaleSchema,
    "child": ChildSchema,
    "elder": ElderSchema,
    "merchant": MerchantSchema,
    "guard": GuardSchema,
    "farmer": FarmerSchema,
    "blacksmith": BlacksmithSchema,
    "soldier": SoldierSchema,
    "elf": ElfSchema,
    "orc": OrcSchema,
    "goblin": GoblinSchema,
    "dwarf": DwarfSchema,
    "dragon": DragonSchema,
    "dog": DogSchema,
    "cat": CatSchema,
    "horse": HorseSchema,
    "cow": CowSchema,
    "deer": DeerSchema,
    "wolf": WolfSchema,
    "bird": BirdSchema,
    "fish": FishSchema,
    "coin": CoinSchema,
    "gem": GemSchema,
    "key": KeySchema,
    "scroll": ScrollSchema,
    "potion": PotionSchema,
    "treasure_chest": TreasureChestSchema,
    "artifact": ArtifactSchema,
    "terrain": TerrainSchema,
    "hill": HillSchema,
    "mountain": MountainSchema,
    "cliff": CliffSchema,
    "valley": ValleySchema,
    "cave": CaveSchema,
    "ground_tile": GroundTileSchema,
    "road_tile": RoadTileSchema,
    "path_tile": PathTileSchema,
    "river_tile": RiverTileSchema,
    "dungeon_tile": DungeonTileSchema,
    "game_background_2d": GameBackground2DSchema,
}

ASSET_TYPE_ALIASES = {
    "storage_tank": "tank",
    "industrial_tank": "tank",
    "fuel_tank": "tank",
}

def validate_asset_params(data: dict) -> AssetParams:
    """Parses and validates arbitrary dictionary data into the appropriate schema model."""
    asset_type = data.get("asset_type")
    if not asset_type:
        raise ValueError("Field 'asset_type' is required to validate parameters.")

    if isinstance(asset_type, str):
        asset_type = asset_type.strip().lower().replace("-", "_").replace(" ", "_")
        asset_type = ASSET_TYPE_ALIASES.get(asset_type, asset_type)

    schema_model = SCHEMA_BY_ASSET_TYPE.get(asset_type)
    if schema_model is None:
        known_types = ", ".join(SCHEMA_BY_ASSET_TYPE.keys())
        raise ValueError(f"Unknown asset_type: '{asset_type}'. Must be one of: {known_types}.")

    normalized_data = dict(data)
    normalized_data["asset_type"] = asset_type
    return schema_model(**normalized_data)
