import type {RoomDefinition} from './house/types';
export type OriginalArtwork={room:string;label:string;backgrounds:string[];selected:string};
export function originalArtwork(room:RoomDefinition,zone:string,poolDrained:boolean):OriginalArtwork {
 const selected=room.id==='connected_hall'&&zone==='Upstairs landing'?'011':room.id==='pool'&&poolDrained?'002':room.backgrounds[0];
 return {room:room.id,label:zone,backgrounds:room.backgrounds,selected};
}
