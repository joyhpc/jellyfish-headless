/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
/**
 * 剧本优化请求（基于一致性检查结果）。
 */
export type ScriptOptimizeRequest = {
    /**
     * 原文剧本文本
     */
    script_text: string;
    /**
     * 一致性检查输出（ScriptConsistencyCheckResult 序列化）
     */
    consistency: Record<string, any>;
};

