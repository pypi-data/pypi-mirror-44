# elist
>__handle list ,nested list tree__

# install
>__pip3 install elist__

## _class_ ListTree

__1. \_\_init\_\_(alist)__
--------------------------

        from elist.elist import *
        from xdict.jprint import pobj
        from xdict.jprint import pdir
        l = [1, [4], 2, [3, [5, 6]]]
        ltree = ListTree(l)

![](elist/Images/ListTree.__init__.0.png)

__2. \_\_repr\_\___
-------------------

        l
        ltree
        pobj(ltree.showlog)

![](elist/Images/ListTree.__repr__.0.png)


__3. tree(**kwargs)__
---------------------

        pathlists = ltree.tree()
        pathlists = ltree.tree(leaf_only=True)
        pathlists = ltree.tree(leaf_only=True,from_lv=1,to_lv=2)
        pathlists = ltree.tree(non_leaf_only=True)

![](elist/Images/ListTree.tree.0.png)

__4. flatten()__
----------------

        flat = ltree.flatten()
        flat
        ltree.flatWidth
        ltree.depth

![](elist/Images/ListTree.flatten.0.png)

__5. dig(howmanysteps)__
------------------------

        depthfirst = ltree.dig()
        depthfirst = ltree.dig(2)
        depthfirst = ltree.dig(5)

![](elist/Images/ListTree.dig.0.png)


__6. level(whichlevel,**kwargs)__
---------------------------------

        level = ltree.level(1)
        level = ltree.level(1,leaf_only=True)
        level = ltree.level(1,non_leaf_only=True)
        level = ltree.level(2)
        level = ltree.level(3)
        
![](elist/Images/ListTree.level.0.png)

__7. include(\*pathlist,**kwargs)__
-----------------------------------

        l[3][1][0]
        ltree.include(3,1,0)
        l[3][1][2]
        ltree.include(pathlist = [3,1,2])
        
![](elist/Images/ListTree.include.0.png)

__8. \_\_getitem\_\_(\*pathlist)__
----------------------------------

        ltree[1,0]
        l[1][0]
        ltree[3,1,1]
        l[3][1][1]

![](elist/Images/ListTree.__getitem__.0.png)

__9A. search(value,**kwargs)__
-----------------------------

        from xdict.TestLib.genrand import gen_random_recursive_only_list_data as randlist
        # lets generate a l for test,l is a big nested-list
        l = randlist()
        #the l looks like the below:
 
![](elist/Images/ListTree.search.0.png)

        #you can see the value "v_4" appears in different levels of the nested-list:

<img src="elist/Images/ListTree.search.1.png" height="400">

        ltree = ListTree(l)
        pathlists = ltree.search('v_4')
        pathlists.__len__()
        #we will found 125 match

<img src="elist/Images/ListTree.search.2.png" height="400">
 
        #......
<img src="elist/Images/ListTree.search.3.png" height="400">

        l[0]
        l[4][2][1][0][0][3]
        l[4][2][1][0][0][19][11]
        l[11][3]

<img src="elist/Images/ListTree.search.4.png" width="400">


__9B. cond_search(value,**kwargs)__
-----------------------------------

        pl1=ltree.search('v_4')
        pl1.__len__() 
        #we found 125 match of "v_4"
        pl2=ltree.search('v_8')
        pl2.__len__()
        #we found 117 match of "v_8"

        #the next we need to found "v_4" or "v_8" whose pathlist includes <14>, and the <14> appears at index <4> in the pathlist
        def cond_func(ele_value,ele_pathlist,position):
            cond1 = ("4" in ele_value) | ("8" in ele_value)
            cond2 = (14 in ele_pathlist)
            cond3 = False
            if(cond2):
                cond3 = (ele_pathlist.index(14) == position)
            else:
                pass
            return(cond1 & cond2 & cond3)

        position = 4
        pl = ltree.cond_search(cond_func=cond_func,cond_func_args=[position])

<img src="elist/Images/ListTree.cond_search.0.png">

        #verify the values

<img src="elist/Images/ListTree.cond_search.1.png">



__ListTree lquery APIs:__


-----------------------------------------------------------------------
>├──10. [ancestor_paths](elist/Images/ListTree.ancestors.0.png)  <br>
├──11. [ancestors](elist/Images/ListTree.ancestors.0.png)  <br>
├──12. [parent_path](elist/Images/ListTree.parent.0.png)  <br>
├──13. [parent](elist/Images/ListTree.parent.0.png)  <br>
├──14. [descendant_paths](elist/Images/ListTree.descendants.1.png)  <br>
├──15. [descendants](elist/Images/ListTree.descendants.1.png)  <br>
├──16. [prevSibPath](elist/Images/ListTree.prevSib.0.png)  <br>
├──17. [prevSibling](elist/Images/ListTree.prevSib.0.png)  <br>
├──18. [nextSibPath](elist/Images/ListTree.nextSib.0.png)  <br>
├──19. [nextSibling](elist/Images/ListTree.nextSib.0.png)  <br>
├──20. [lsib_path](elist/Images/ListTree.prevSib.0.png)  <br>
├──21. [lsib](elist/Images/ListTree.prevSib.0.png)  <br>
├──22. [rsib_path](elist/Images/ListTree.nextSib.0.png)  <br>
├──23. [rsib](elist/Images/ListTree.nextSib.0.png)  <br>
├──24. [sib_paths](elist/Images/ListTree.sibs.0.png)  <br>
├──25. [sibs](elist/Images/ListTree.sibs.0.png)  <br>
├──26. [someSibPaths](elist/Images/ListTree.someSibs.0.png)  <br>
├──27. [someSibs](elist/Images/ListTree.someSibs.0.png)  <br>
├──28. [some_sib_paths](elist/Images/ListTree.someSibs.0.png)  <br>
├──29. [some_sibs](elist/Images/ListTree.someSibs.0.png)  <br>
├──30. [whichSibPath](elist/Images/ListTree.whichSib.0.png)  <br>
├──31. [whichSib](elist/Images/ListTree.whichSib.0.png)  <br>
├──32. [which_sib_path](elist/Images/ListTree.which_sib.0.png)  <br>
├──33. [which_sib](elist/Images/ListTree.which_sib.0.png)  <br>
├──34. [precedingSibPaths](elist/Images/ListTree.precedingSibs.0.png)  <br>
├──35. [precedingSibs](elist/Images/ListTree.precedingSibs.0.png)  <br>
├──36. [preceding_sib_paths](elist/Images/ListTree.precedingSibs.0.png)  <br>
├──37. [preceding_sibs](elist/Images/ListTree.precedingSibs.0.png)  <br>
├──38. [followingSibPaths](elist/Images/ListTree.followingSibs.0.png)  <br>
├──39. [followingSibs](elist/Images/ListTree.followingSibs.0.png)  <br>
├──40. [following_sib_paths](elist/Images/ListTree.followingSibs.0.png)  <br>
├──41. [following_sibs](elist/Images/ListTree.followingSibs.0.png)  <br>
├──42. [lcin_path](elist/Images/ListTree.lcin.0.png)  <br>
├──43. [lcin](elist/Images/ListTree.lcin.0.png)  <br>
├──44. [rcin_path](elist/Images/ListTree.rcin.0.png)  <br>
├──45. [rcin](elist/Images/ListTree.rcin.0.png)  <br>
├──46. [son_paths](elist/Images/ListTree.sons.0.png)  <br>
├──47. [sons](elist/Images/ListTree.sons.0.png)  <br>
├──48. [total](elist/Images/ListTree.PARAMS.0.png)  <br>
├──49. [maxLevelWidth](elist/Images/ListTree.PARAMS.0.png)  <br>
├──50. [depth](elist/Images/ListTree.PARAMS.0.png)  <br>
├──51. [flatWidth](elist/Images/ListTree.PARAMS.0.png)  <br>

-----------------------------------------------------------------------

## _elist_ functions

-----------------------------------------------------------------------
>├──0. [select_some](elist/Images/select.0.png)  <br>
├──1. [select_seqs](elist/Images/select.0.png)  <br>
├──1. [select_seqs_not](elist/Images/select_seqs_not.0.png)  <br>
├──1. [select_seqs_keep_order](elist/Images/select_seqs_keep_order.0.png)  <br>
├──1. [select_indexes](elist/Images/select.0.png)  <br>
├──1. [select_odds](elist/Images/select_odds.0.png)  <br>
├──1. [select_evens](elist/Images/select_evens.0.png)  <br>
├──1. [select_interval](elist/Images/select_interval.0.png)  <br>
├──1. [cond_select_all](elist/Images/cond_select_all.0.png)  <br>
├──1. [cond_select_all2](elist/Images/cond_select_all2.0.png)  <br>
├──1. [cond_select_values_all](elist/Images/cond_select_all.0.png)  <br>
├──1. [cond_select_values_all2](elist/Images/cond_select_all2.0.png)  <br>
├──1. [cond_select_indexes_all](elist/Images/cond_select_indexes_all.0.png)  <br>
├──1. [cond_select_indexes_all2](elist/Images/cond_select_indexes_all2.0.png)  <br>
├──1. [loose_in](elist/Images/loose_in.0.png)  <br>
├──1. [select_loose_in](elist/Images/loose_in.0.png)  <br>
├──1. [select_strict_in](elist/Images/strict_in.0.png)  <br>
├──1. [regex_in](elist/Images/regex_in.0.png)  <br>
├──1. [select_regex_in](elist/Images/regex_in.0.png)  <br>
├──2. [append](elist/Images/append.0.png)  <br>
├──3. [append_some](elist/Images/append_some.0.png)  <br>
├──4. [prepend](elist/Images/prepend.0.png)  <br>
├──5. [prepend_some](elist/Images/unshift.0.png)  <br>
├──5. [unshift](elist/Images/unshift.0.png)  <br>
├──6. [extend](elist/Images/extend.0.png)  <br>
├──6. [push](elist/Images/push.0.png)  <br>
├──7. [concat](elist/Images/concat.0.png)  <br>
├──7. [concat_some](elist/Images/concat.0.png)  <br>
├──7. [concat_seqs](elist/Images/concat_seqs.0.png)  <br>
├──8. [prextend](elist/Images/prextend.0.png)  <br>
├──9. [car](elist/Images/carcdr.0.png)  <br>
├──10. [cdr](elist/Images/carcdr.0.png)  <br>
├──11. [cons](elist/Images/cons.0.png)  <br>
├──12. [insert](elist/Images/insert.0.png)  <br>
├──13. [insert_some](elist/Images/insert_some.0.png)  <br>
├──14. [insert_many](elist/Images/insert_many.0.png)  <br>
├──14. [insert_section](elist/Images/insert_section.0.png)  <br>
├──14. [insert_sections_some](elist/Images/insert_section.0.png)  <br>
├──14. [insert_sections_many](elist/Images/insert_sections_many.0.png)  <br>
├──14. [reorder_sub](elist/Images/reorder_sub.0.png)  <br>
├──14. [sort](elist/Images/sort.0.png)  <br>
├──15. [batsorted](elist/Images/batsorted.0.png)  <br>
├──15. [batexec](elist/Images/batexec.0.png)  <br>
├──15. [sortDictList](elist/Images/sortDictList.0.png)  <br>
├──15. [sortDictList2](elist/Images/sortDictList2.0.png)  <br>
├──16. [index_first](elist/Images/index_first.0.png)  <br>
├──17. [array_index](elist/Images/index_first.0.png)  <br>
├──18. [indexOf](elist/Images/index_first.0.png)  <br>
├──19. [index_firstnot](elist/Images/index_firstnot.0.png)  <br>
├──20. [array_indexnot](elist/Images/index_firstnot.0.png)  <br>
├──21. [indexOfnot](elist/Images/index_firstnot.0.png)  <br>
├──22. [index_last](elist/Images/index_last.0.png)  <br>
├──24. [lastIndexOf](elist/Images/index_last.0.png)  <br>
├──25. [index_lastnot](elist/Images/index_lastnot.0.png)  <br>
├──26. [lastIndexOfnot](elist/Images/index_lastnot.0.png)  <br>
├──27. [index_which](elist/Images/index_which.0.png)  <br>
├──28. [index_whichnot](elist/Images/index_whichnot.0.png)  <br>
├──29. [indexes_all](elist/Images/indexes_all.0.png)  <br>
├──30. [indexes_allnot](elist/Images/indexes_all.0.png)  <br>
├──31. [indexes_some](elist/Images/indexes_some.0.png)  <br>
├──32. [indexes_somenot](elist/Images/indexes_some.0.png)  <br>
├──33. [indexes_seqs](elist/Images/indexes_seqs.0.png)  <br>
├──34. [indexes_seqsnot](elist/Images/indexes_seqs.0.png)  <br>
├──35. [first_continuous_indexes_slice](elist/Images/firstlast_continuous_indexes_slice.0.png)  <br>
├──36. [first_continuous_indexesnot_slice](elist/Images/firstlast_continuous_indexes_slice.0.png)  <br>
├──37. [last_continuous_indexes_slice](elist/Images/firstlast_continuous_indexes_slice.0.png)  <br>
├──38. [last_continuous_indexesnot_slice](elist/Images/firstlast_continuous_indexes_slice.0.png)  <br>
├──39. [which_continuous_indexes_slice](elist/Images/which_continuous_indexes_slice.0.png)  <br>
├──40. [which_continuous_indexesnot_slice](elist/Images/which_continuous_indexes_slice.0.png)  <br>
├──41. [some_continuous_indexes_slices](elist/Images/all_some_seqs_continuous_indexes_slices.0.png)  <br>
├──42. [some_continuous_indexesnot_slices](elist/Images/all_some_seqs_continuous_indexes_slices.0.png)  <br>
├──43. [seqs_continuous_indexes_slices](elist/Images/all_some_seqs_continuous_indexes_slices.0.png)  <br>
├──44. [seqs_continuous_indexesnot_slices](elist/Images/all_some_seqs_continuous_indexes_slices.0.png)  <br>
├──45. [all_continuous_indexes_slices](elist/Images/all_some_seqs_continuous_indexes_slices.0.png)  <br>
├──46. [all_continuous_indexesnot_slices](elist/Images/all_some_seqs_continuous_indexes_slices.0.png)  <br>
├──47. [shift](elist/Images/shift.0.png)  <br>
├──48. [pop](elist/Images/pop.0.png)  <br>
├──48. [cond_pop](elist/Images/cond_pop.0.png)  <br>
├──49. [pop_range](elist/Images/pop_range.0.png)  <br>
├──50. [pop_some](elist/Images/pop_some.0.png)  <br>
├──51. [pop_indexes](elist/Images/pop_indexes.0.png)  <br>
├──52. [array_remove](elist/Images/array_remove.0.png)  <br>
├──53. [remove_first](elist/Images/remove_first.0.png)  <br>
├──54. [array_removenot](elist/Images/array_removenot.0.png)  <br>
├──55. [remove_firstnot](elist/Images/remove_firstnot.0.png)  <br>
├──56. [remove_last](elist/Images/remove_last.0.png)  <br>
├──57. [remove_lastnot](elist/Images/remove_lastnot.0.png)  <br>
├──58. [remove_which](elist/Images/remove_which.0.png)  <br>
├──59. [remove_whichnot](elist/Images/remove_whichnot.0.png)  <br>
├──60. [remove_some](elist/Images/remove_some.0.png)  <br>
├──61. [remove_somenot](elist/Images/remove_somenot.0.png)  <br>
├──62. [remove_seqs](elist/Images/remove_seqs.0.png)  <br>
├──63. [remove_seqsnot](elist/Images/remove_seqsnot.0.png)  <br>
├──64. [remove_all](elist/Images/remove_all.0.png)  <br>
├──65. [remove_allnot](elist/Images/remove_allnot.0.png)  <br>
├──66. [remove_many](elist/Images/remove_many.0.png)  <br>
├──67. [remove_manynot](elist/Images/remove_manynot.0.png)  <br>
├──67. [cond_remove_all](elist/Images/cond_remove_all.0.png)  <br>
├──67. [cond_remove_seqs](elist/Images/cond_remove_seqs.0.png)  <br>
├──67. [cond_remove_some](elist/Images/cond_remove_some.0.png)  <br>
├──68. [init](elist/Images/init.0.png)  <br>
├──68. [initWith](elist/Images/initWith.0.png)  <br>
├──68. [init_range](elist/Images/init_range.0.png)  <br>
├──68. [initRange](elist/Images/init_range.0.png)  <br>
├──69. [intlize](elist/Images/init.0.png)  <br>
├──70. [strlize](elist/Images/init.0.png)  <br>
├──71. [array_from](elist/Images/array_from.0.png)  <br>
├──72. [array_of](elist/Images/init.0.png)  <br>
├──73. [deepcopy](elist/Images/copy.0.png)  <br>
├──74. [copy_within](elist/Images/copy.0.png)  <br>
├──75. [copyWithin](elist/Images/copy.0.png)  <br>
├──76. [reverse](elist/Images/reverse.0.png)  <br>
├──77. [comprise](elist/Images/comprise.0.png)  <br>
├──78. [entries](elist/Images/entries.0.png)  <br>
├──79. [includes](elist/Images/entries.0.png)  <br>
├──80. [toString](elist/Images/entries.0.png)  <br>
├──81. [toSource](elist/Images/entries.0.png)  <br>
├──82. [splice](elist/Images/splice.0.png)  <br>
├──83. [slice](elist/Images/slice.0.png)  <br>
├──84. [join](elist/Images/join.0.png)  <br>
├──85. [join2](elist/Images/join.0.png)  <br>
├──86. [htmljoin](elist/Images/join.0.png)  <br>
├──87. [uniqualize](elist/Images/uniqualize.0.png)  <br>
├──87. [cond_uniqualize\<0\>](elist/Images/cond_uniqualize.0.png)  <br>
├──87. [cond_uniqualize\<1\>](elist/Images/cond_uniqualize.1.png)  <br>
├──88. [interleave](elist/Images/interleave.0.png)  <br>
├──89. [for_each](elist/Images/forEach.0.png)  <br>
├──90. [forEach](elist/Images/forEach.0.png)  <br>
├──91. [some](elist/Images/some.0.png)  <br>
├──92. [every](elist/Images/every.0.png)  <br>
├──92. [every2](elist/Images/every2.0.png)  <br>
├──93. [fill](elist/Images/fill.0.png)  <br>
├──94. [filter](elist/Images/filter.0.png)  <br>
├──94. [filter2](elist/Images/filter2.0.png)  <br>
├──95. [find_first](elist/Images/find_first.0.png)  <br>
├──96. [find](elist/Images/find_first.0.png)  <br>
├──97. [find_firstnot](elist/Images/find_firstnot.0.png)  <br>
├──98. [findnot](elist/Images/find_firstnot.0.png)  <br>
├──99. [find_last](elist/Images/find_last.0.png)  <br>
├──100. [find_lastnot](elist/Images/find_lastnot.0.png)  <br>
├──101. [find_which](elist/Images/find_which.0.png)  <br>
├──102. [find_whichnot](elist/Images/find_whichnot.0.png)  <br>
├──103. [find_seqs](elist/Images/find_seqs.0.png)  <br>
├──104. [find_some](elist/Images/find_seqs.0.png)  <br>
├──105. [find_seqsnot](elist/Images/find_seqsnot.0.png)  <br>
├──106. [find_somenot](elist/Images/find_seqsnot.0.png)  <br>
├──107. [find_all](elist/Images/find_all.0.png)  <br>
├──107. [find_all2](elist/Images/find_all2.0.png)  <br>
├──108. [find_allnot](elist/Images/find_allnot.0.png)  <br>
├──109. [array_map](elist/Images/array_map.0.png)  <br>
├──110. [array_map2](elist/Images/array_map2.0.png)  <br>
├──111. [array_dualmap](elist/Images/array_dualmap.0.png)  <br>
├──112. [array_dualmap2](elist/Images/array_dualmap2.0.png)  <br>
├──112. [mapfivo(ol,\*\*kwargs)](elist/Images/.png)  <br>
├──112. [mapfiv(ol,map_func_args,\*\*kwargs)](elist/Images/.png)  <br>
├──112. [mapfio(ol,\*\*kwargs)](elist/Images/.png)  <br>
├──112. [mapfvo(ol,\*\*kwargs)](elist/Images/.png)  <br>
├──112. [mapivo(ol,map_func,\*\*kwargs)](elist/Images/.png)  <br>
├──112. [mapfi(ol,map_func_args,\*\*kwargs)](elist/Images/.png)  <br>
├──112. [mapfv(ol,map_func_args,\*\*kwargs)](elist/Images/.png)  <br>
├──112. [mapfo(ol,\*\*kwargs)](elist/Images/.png)  <br>
├──112. [mapiv(ol,map_func,map_func_args)](elist/Images/.png)  <br>
├──112. [mapiv2(ol,map_func,\*args,\*\*kwargs)](elist/Images/.png)  <br>
├──112. [mapio(ol,map_func,\*\*kwargs)](elist/Images/.png)  <br>
├──112. [mapvo(ol,map_func,\*\*kwargs)](elist/Images/.png)  <br>
├──112. [mapf(ol,map_func_args,\*\*kwargs)](elist/Images/.png)  <br>
├──112. [mapi(ol,map_func,map_func_args)](elist/Images/.png)  <br>
├──112. [mapv(ol,map_func,map_func_args)](elist/Images/.png)  <br>
├──112. [mapo(ol,map_func,\*\*kwargs)](elist/Images/.png)  <br>
├──113. [reduce_left](elist/Images/reduce_left.0.png)  <br>
├──114. [array_reduce ](elist/Images/reduce_left.0.png)  <br>
├──115. [reduceLeft](elist/Images/reduce_left.0.png)  <br>
├──116. [reduce_right](elist/Images/reduce_right.0.png)  <br>
├──117. [reduceRight](elist/Images/reduce_right.0.png)  <br>
├──118. [diff_indexes](elist/Images/diff_and_same.0.png)  <br>
├──119. [diff_values](elist/Images/diff_and_same.0.png)  <br>
├──120. [same_indexes](elist/Images/diff_and_same.0.png)  <br>
├──121. [same_values](elist/Images/diff_and_same.0.png)  <br>
├──122. [value_indexes_mapping](elist/Images/diff_and_same.0.png)  <br>
├──122. [cond_value_indexes_mapping](elist/Images/cond_value_indexes_mapping.0.png)  <br>
├──123. [getitem_via_pathlist](elist/Images/get.0.png)  <br>
├──124. [getitem_via_pathlist2](elist/Images/get.0.png)  <br>
├──125. [getitem_via_sibseqs](elist/Images/get.0.png)  <br>
├──126. [setitem_via_pathlist](elist/Images/set_del.0.png)  <br>
├──127. [setitem_via_sibseqs](elist/Images/set_del.0.png)  <br>
├──128. [delitem_via_pathlist](elist/Images/set_del.0.png)  <br>
├──129. [delitem_via_sibseqs](elist/Images/set_del.0.png)  <br>
├──130. [is_leaf](elist/Images/is_leaf.0.png)  <br>
├──131. [replace_seqs](elist/Images/replace_seqs.0.png)  <br>
├──132. [replace_some](elist/Images/replace_some.0.png)  <br>
├──133. [replace_value_some](elist/Images/replace_value_some.0.png)  <br>
├──134. [replace_value_seqs](elist/Images/replace_value_seqs.0.png)  <br>
├──134. [cond_replace_value_all](elist/Images/cond_replace_value_all.0.png)  <br>
├──134. [cond_replace_value_seqs](elist/Images/cond_replace_value_seqs.0.png)  <br>
├──134. [cond_replace_value_some](elist/Images/cond_replace_value_some.0.png)  <br>
├──135. [rangize](elist/Images/rangize.0.png)  <br>
├──135. [rangize_supplement](elist/Images/rangize_supplement.0.png) <br>
├──135. [rangize_fullfill](elist/Images/rangize_fullfill.0.png) <br>
├──135. [range_compress](elist/Images/range_compress.0.png)  <br>
├──135. [range_decompress](elist/Images/range_decompress.0.png)  <br>
├──136. [broken_seqs](elist/Images/broken.0.png)  <br>
├──137. [broken_some](elist/Images/broken.0.png)  <br>
├──137. [brkl2kvlist](elist/Images/brkl2kvlist.0.png)  <br>
├──137. [divide](elist/Images/divide.0.png)  <br>
├──138. [classify](elist/Images/classify.0.png)  <br>
├──139. [classifyDictList](elist/Images/classifyDictList.0.png)  <br>
├──140. [split](elist/Images/split.0.png)  <br>
├──141. [where](elist/Images/where.0.png)  <br>
├──142. [where_index_interval](elist/Images/where.0.png)  <br>
├──143. [index_interval](elist/Images/where.0.png)  <br>
├──142. [where_value_interval](elist/Images/value_interval.0.png)  <br>
├──143. [value_interval](elist/Images/value_interval.0.png)  <br>
├──144. [upper_bound](elist/Images/upper_bound.0.png)  <br>
├──145. [lower_bound](elist/Images/lower_bound.0.png)  <br>
├──146. [matrix_map](elist/Images/matrix_map.0.png)  <br>
├──146. [is_matrix](elist/Images/is_matrix.0.png)  <br>
├──146. [transpose](elist/Images/transpose.0.png)  <br>
├──147. [mat2wfs](elist/Images/mat2wfs.0.png)  <br>
├──148. [wfs2mat](elist/Images/wfs2mat.0.png)  <br>
├──149. [wfsmat2dfs](elist/Images/wfsmat2dfs.0.png)  <br>
├──150. [dfs2wfsmat](elist/Images/dfs2wfsmat.0.png)  <br>
├──151. [wfs2dfs](elist/Images/wfs2dfs.0.png)  <br>
├──152. [dfs2wfs](elist/Images/dfs2wfs.0.png)  <br>
├──153. [get_dfs](elist/Images/get_dfs.0.png)  <br>
├──154. [get_wfsmat](elist/Images/get_wfsmat.0.png)  <br>
├──155. [get_wfs](elist/Images/get_wfs.0.png)  <br>
├──156. [rand_some_indexes](elist/Images/rand_some_indexes.0.png)  <br>
├──157. [rand_sub](elist/Images/rand_sub.0.png)  <br>
├──158. [repeat_every](elist/Images/repeat_every.0.png)  <br>
├──159. [reindex](elist/Images/reindex.0.png)  <br>
├──159. [iswap](elist/Images/iswap.0.png)  <br>
├──159. [vswap](elist/Images/vswap.0.png)  <br>
├──160. [union](elist/Images/union.0.png)  <br>
├──161. [intersection](elist/Images/intersection.0.png)  <br>
├──162. [difference](elist/Images/difference.0.png)  <br>


