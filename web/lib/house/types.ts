export type Point = {x:number;y:number};
export type Walker = Point & {height:number};
export type Navigation = {
 floorHeight:(p:Point,height?:number)=>number;
 canStand:(p:Point,height?:number)=>boolean;
 zone:(p:Walker)=>string;
};
export type Placement = {id:string;definition:string;position:number[];yaw:number;previewOnly?:boolean};
export type Connection = {a:{instance:string;port:string};b:{instance:string;port:string}};
export type HouseData = {start:string;rooms:Placement[];definitions:Record<string,RoomDefinition>;connections:Connection[];spaces?:{id:string;rooms:string[];origin:string}[];portalDepth?:number};

export type RoomDefinition={id:string;label:string;backgrounds:string[];asset:string;sharedAssetLibrary?:string;navigation:string;bounds:{min:number[];max:number[]};spawn:Walker & {yaw:number;pitch:number};geometry?:{[key:string]:unknown;sharedAssets?:SharedAssetInstance[];doors?:DoorDefinition[];doorObstacles?:{min:number[];max:number[]}[]};ports:Port[]};
export type Port={id:string;position:number[];outward:number[];width:number;state:string;height?:number};

export type DoorLeaf={node:string;hinge:number[];openAngle:number;min:number[];max:number[]};
export type DoorDefinition={id:string;label:string;port:string;initialOpen:boolean;leaves:DoorLeaf[]};

export type SharedAssetInstance={id:string;asset:string;matrix:number[];doorNode?:string};
