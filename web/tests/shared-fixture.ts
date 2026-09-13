import {readFile} from 'node:fs/promises';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';
import * as THREE from 'three';
import {instantiateSharedAssets} from '../lib/house/shared-assets';
import type {RoomDefinition} from '../lib/house/types';
export async function loadDoorKit(){
 const bytes=await readFile('../generated/models/doors/standard_doors_v1_compact.glb');
 return (await new GLTFLoader().parseAsync(bytes.buffer.slice(bytes.byteOffset,bytes.byteOffset+bytes.byteLength) as ArrayBuffer,'')).scene;
}
export async function addDoorKit(root:THREE.Object3D,definition:RoomDefinition){
 if(definition.sharedAssetLibrary)instantiateSharedAssets(root,definition,await loadDoorKit());
}
