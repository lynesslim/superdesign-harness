#!/usr/bin/env python3
"""Idempotent: removes any earlier polish-tokens block first.
Write a Novamira execute-php payload that appends the override block to a cloned page via elementor-add-element
(zero-padding root container + html widget). Run the payload with:
  novamira --site <profile> --json --yes run novamira/execute-php --input @apply.json
Then clear the Elementor cache for the page (elementor-clear-document-cache, param post_ids)."""
import argparse, json
ap = argparse.ArgumentParser(); ap.add_argument('--page-id', required=True, type=int); ap.add_argument('--css', required=True); ap.add_argument('--out', required=True)
a = ap.parse_args()
html = open(a.css).read()
code = ("$d=json_decode(get_post_meta(%d,'_elementor_data',true),true)?:[]; foreach($d as $e){ if(($e['settings']['_element_id']??'')==='polish-tokens'){ wp_get_ability('novamira/elementor-delete-element')->execute(['post_id'=>%d,'element_id'=>$e['id']]); } } "
        "$h=json_decode(%s); $r=wp_get_ability('novamira/elementor-add-element')->execute(['post_id'=>%d,'parent_id'=>null,"
        "'tree'=>['elType'=>'container','settings'=>['content_width'=>'full','_element_id'=>'polish-tokens',"
        "'padding'=>['unit'=>'px','top'=>'0','right'=>'0','bottom'=>'0','left'=>'0','isLinked'=>true]],"
        "'elements'=>[['elType'=>'widget','widgetType'=>'html','settings'=>['html'=>$h]]]]]); "
        "$c=wp_get_ability('novamira/elementor-clear-document-cache')->execute(['post_ids'=>[%d]]); "
        "return is_wp_error($r)?[$r->get_error_message(),$r->get_error_data()]:$r;") % (a.page_id, a.page_id, json.dumps(json.dumps(html)), a.page_id, a.page_id)
json.dump({'code': code}, open(a.out, 'w'))
print('wrote', a.out)
