import type {createPortals} from './portals';
/** Residency follows declared connections, never overlapping world bounds. */
export function neighboringRooms(graph:ReturnType<typeof createPortals>,space:string){
 const result=new Set(graph.members(space).map(r=>r.id));
 for(const edge of graph.outgoing(space))for(const room of graph.members(edge.to.space))result.add(room.id);
 return result;
}
