import manifest from '../house/generated.json' with {type:'json'};
import {shellNavigation} from './shell-navigation';
export const {floorHeight,canStand,zone}=shellNavigation(manifest.definitions.cellar);
