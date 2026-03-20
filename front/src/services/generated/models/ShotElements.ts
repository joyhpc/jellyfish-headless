/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { DialogueLine } from './DialogueLine';
import type { ShotCharacterInfo } from './ShotCharacterInfo';
import type { ShotPropInfo } from './ShotPropInfo';
import type { ShotSceneInfo } from './ShotSceneInfo';
/**
 * 单镜提取的元素信息（索引 + 细粒度 + 对白/动作）。
 */
export type ShotElements = {
    /**
     * 角色键列表（弱ID）
     */
    character_keys?: Array<string>;
    /**
     * 场景键列表（弱ID）
     */
    scene_keys?: Array<string>;
    /**
     * 服装键列表（弱ID）
     */
    costume_keys?: Array<string>;
    /**
     * 道具键列表（弱ID）
     */
    prop_keys?: Array<string>;
    /**
     * 角色细粒度提取
     */
    characters_detailed?: Array<ShotCharacterInfo>;
    /**
     * 道具细粒度提取
     */
    props_detailed?: Array<ShotPropInfo>;
    /**
     * 场景细粒度提取
     */
    scene_detailed?: (ShotSceneInfo | null);
    /**
     * 结构化对白列表
     */
    dialogue_lines?: Array<DialogueLine>;
    /**
     * 动作/场景描述
     */
    actions?: Array<string>;
    /**
     * 推断的镜头类型：close-up, wide-shot, tracking 等
     */
    shot_type_hints?: Array<string>;
    /**
     * 各类别置信度
     */
    confidence_breakdown?: Record<string, number>;
};

