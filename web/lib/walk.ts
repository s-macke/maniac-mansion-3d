/** Compatibility exports for existing collision tests and tools. */
export type { Point, Walker } from './house/types';
export { EYE_HEIGHT, RADIUS } from './house/navigation';
import { createHouseRuntime } from './house/runtime';
export const {START,moveWalker}=createHouseRuntime('hall');
export { floorHeight, canStand, stairEdges, galleryBoundary } from './rooms/connected_hall';
export { segmentProjection } from './house/geometry';
