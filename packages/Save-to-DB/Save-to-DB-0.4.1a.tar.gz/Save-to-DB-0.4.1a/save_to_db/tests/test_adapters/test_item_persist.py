import datetime
from save_to_db.adapters.utils.adapter_manager import get_adapter_cls

from save_to_db.core.scope import Scope
from save_to_db.core.item import Item
from save_to_db.core.exceptions import (MultipleModelsMatch,
                                        MultipleItemsMatch)
from save_to_db.utils.test_base import TestBase
from itertools import chain



class TestItemPersist(TestBase):
    """ Contains tests for persisting items into database. """
    
    ModelGeneralOne = None
    ModelGeneralTwo = None
    
    ModelManyRefsOne = None
    ModelManyRefsTwo = None
    
    ModelAutoReverseOne = None
    ModelAutoReverseTwoA = None
    ModelAutoReverseTwoB = None
    ModelAutoReverseThreeA = None
    ModelAutoReverseThreeB = None
    ModelAutoReverseFourA = None
    ModelAutoReverseFourB = None


    def test_persist_single_item_no_related(self):
        
        class ItemGeneralOne(Item):
            model_cls = self.ModelGeneralOne
            creators = [{'f_integer'}]
            getters = [{'f_float'}, {'f_string', 'f_text'},
                       {'f_date'}]
        
        # need this for `ItemGeneralOne` (related field)
        class ItemGeneralTwo(Item):
            model_cls = self.ModelGeneralTwo
                
        persister = self.persister
        
        # creating and updating first model ------------------------------------
        
        # cannot create or get
        item = ItemGeneralOne(f_string='str-one')
        items, model_lists = persister.persist(item)
        self.assertFalse(items)
        self.assertFalse(model_lists)
        
        # can get but not create and not in database
        item['f_text'] = 'text-one'
        items, model_lists = persister.persist(item)
        self.assertFalse(items)
        self.assertFalse(model_lists)
        
        # can create
        item['f_integer'] = None  # `None` can create
        items, model_lists = persister.persist(item)
        self.assertEqual(len(items), 1)
        self.assertEqual(len(items), len(model_lists))
        models = model_lists[0]
        self.assertEqual(len(models), 1)
        self.assertIs(items[0], item)
        
        self.assertEqual(models[0].f_string, 'str-one')
        self.assertEqual(models[0].f_text, 'text-one')
        self.assertEqual(models[0].f_integer, None)
        self.assertEqual(models[0].f_date, None)
        
        # can update (`{'f_string', 'f_text'}` are the getters)
        
        # `f_date=None` will be used as getter later
        item['f_date'] = '2010-10-10'
        
        item['f_integer'] = '100'
        items, model_lists = persister.persist(item)
        self.assertEqual(len(items), 1)
        self.assertEqual(len(items), len(model_lists))
        models = model_lists[0]
        self.assertEqual(len(models), 1)
        self.assertIs(items[0], item)
        
        # checking that model got the same values
        self.assertEqual(models[0].f_string, 'str-one')
        self.assertEqual(models[0].f_text, 'text-one')
        self.assertEqual(models[0].f_integer, 100)
        self.assertEqual(models[0].f_date, datetime.date(2010, 10, 10))
        
        first_model = models[0]
        
        # creating second model ------------------------------------------------
        
        item = ItemGeneralOne(f_integer='200', f_string='str-one')
        items, model_lists = persister.persist(item)
        self.assertEqual(len(items), 1)
        self.assertEqual(len(items), len(model_lists))
        models = model_lists[0]
        self.assertEqual(len(models), 1)
        self.assertIs(items[0], item)
        
        second_model = models[0]
        self.assertNotEqual(models[0], first_model)
        self.assertEqual(models[0].f_string, 'str-one')
        self.assertEqual(models[0].f_integer, 200)
        
        # updating first and second model --------------------------------------
        
        # updating second model
        item = ItemGeneralOne(f_date=None)  # `None` value can be used
        items, model_lists = persister.persist(item)
        self.assertEqual(len(models), 1)
        self.assertIs(items[0], item)
        models = model_lists[0]
        self.assertEqual(len(models), 1)
        self.assertIs(items[0], item)
        
        self.assertEqual(models[0], second_model)
        self.assertEqual(models[0].f_integer, 200)
        self.assertEqual(models[0].f_string, 'str-one')
        self.assertEqual(models[0].f_text, None)
        self.assertIs(models[0].f_boolean, None)
        self.assertIs(models[0].f_date, None)
        
        # updating second model
        self.assertIs(first_model.f_boolean, None)  # will be `True` later
        item['f_string'] = 'str-one'
        item['f_text'] = 'text-one'
        item['f_boolean'] = True
        item['f_date'] = '2015-10-10'
        
        items, model_lists = persister.persist(item)
        self.assertEqual(len(items), 1)
        self.assertEqual(len(items), len(model_lists))
        models = model_lists[0]
        self.assertEqual(len(models), 1)
        self.assertIs(items[0], item)
        
        self.assertEqual(models[0], first_model)
        self.assertEqual(models[0].f_integer, 100)
        self.assertEqual(models[0].f_string, 'str-one')
        self.assertEqual(models[0].f_text, 'text-one')
        self.assertIs(models[0].f_boolean, True)
        self.assertEqual(models[0].f_date, datetime.date(2015, 10, 10))

        # return boolean to `None`
        item['f_boolean'] = None
        items, (models,) = persister.persist(item)
        self.assertEqual(models[0], first_model)
        self.assertIs(models[0].f_boolean, None)
        
    
    def test_persist_single_item_with_single_related(self):
        model_one_cls = self.ModelGeneralOne
        model_two_cls = self.ModelGeneralTwo
        
        class ItemGeneralOne(Item):
            model_cls = self.ModelGeneralOne
            creators = [{'f_integer', 'two_1_1'}]
            getters = [{'f_integer', 'two_1_1'},
                       {'f_float'},
                       {'f_string', 'f_text'},
                       {'f_date'}]
        
        class ItemGeneralTwo(Item):
            model_cls = self.ModelGeneralTwo
            creators = [{'f_integer'}]
            getters = [{'f_integer'}]
        
        persister = self.persister
        
        # cannot create any items
        # 'two_1_1' is not present 
        item_one = ItemGeneralOne(f_integer='100')
        items, model_lists = persister.persist(item_one)
        self.assertEqual(len(items), 0)
        self.assertEqual(len(items), len(model_lists))
        
        # 'two_1_1' cannot be created
        item_two = ItemGeneralTwo(f_float='20.20')
        items, model_lists = persister.persist(item_two)
        self.assertEqual(len(items), 0)
        self.assertEqual(len(items), len(model_lists))
        
        item_one['two_1_1'] = item_two
        items, model_lists = persister.persist(item_one)
        self.assertEqual(len(items), 0)
        self.assertEqual(len(items), len(model_lists))
        
        self.assertEqual(len(self.get_all_models(model_one_cls)), 0)
        self.assertEqual(len(self.get_all_models(model_two_cls)), 0)
        
        # 'two_1_1' can be created
        item_two['f_integer'] = '200'
        del item_one['f_integer']  # won't be persisted
        items, model_lists = persister.persist(item_one)
        self.assertEqual(len(items), 0)
        self.assertEqual(len(items), len(model_lists))
        
        self.assertEqual(len(self.get_all_models(model_one_cls)), 0)
        # but `item_two` was persisted
        models_two = self.get_all_models(model_two_cls)
        self.assertEqual(len(models_two), 1)
        self.assertEqual(models_two[0].f_integer, 200)
        self.assertEqual(models_two[0].f_float, 20.2)
        
        # persisting item_one with updating existing model
        self.assertIs(models_two[0].f_boolean, None)
        item_one['f_integer'] = '100'
        item_two['f_boolean'] = True
        
        items, model_lists = persister.persist(item_one)
        self.assertEqual(len(items), 1)
        self.assertEqual(len(items), len(model_lists))
        self.assertEqual(len(model_lists), 1)
        models = model_lists[0]
        self.assertEqual(len(models), 1)
        self.assertIs(items[0], item_one)
        
        self.assertEqual(models[0].f_integer, 100)
        self.assertIsNotNone(models[0].two_1_1)
        self.assertIsNotNone(models[0].two_1_1.f_integer, 200)
        self.assertIsNotNone(models[0].two_1_1.f_float, 20.2)
        self.assertIs(models[0].two_1_1.f_boolean, True)
        
        self.assertEqual(len(self.get_all_models(model_one_cls)), 1)
        self.assertEqual(len(self.get_all_models(model_two_cls)), 1)
        
        # persisting using related item as filter
        del item_two['one_1_1']  # old item
        item_one = ItemGeneralOne(f_integer='100', two_1_1=item_two)
        item_one['f_boolean'] = False
        
        items, model_lists = persister.persist(item_one)
        
        self.assertEqual(len(items), 1)
        self.assertEqual(len(items), len(model_lists))
        self.assertEqual(len(model_lists), 1)
        models = model_lists[0]
        self.assertEqual(len(models), 1)
        self.assertIs(items[0], item_one)
        self.assertIs(models[0].f_boolean, False)
        
        self.assertEqual(len(self.get_all_models(model_one_cls)), 1)
        self.assertEqual(len(self.get_all_models(model_two_cls)), 1)
    
    
    def test_persist_single_item_with_x_to_many_related(self):
        class ItemGeneralOne(Item):
            model_cls = self.ModelGeneralOne
            creators = [{'f_string'}]
            getters = [{'two_1_x'}, {'f_string'}]
        
        class ItemGeneralTwo(Item):
            model_cls = self.ModelGeneralTwo
            creators = [{'f_string'}]
            getters = [{'f_string'}]
        
        persister = self.persister
        
        # creating first set of items
        item_one_bulk = ItemGeneralOne.Bulk()
        for (item_name, known_names) in [['one', ['first', 'one',]],
                                         ['two', ['second', 'two']]]:
            item_one = item_one_bulk.gen(f_string=item_name)
            for known_name in known_names:
                item_one['two_1_x'].gen(f_string=known_name)
            
        persister.persist(item_one_bulk)
        
        # creating second set of items
        # (`item_one` instance with name "one" must match 
        #  item with name "one_more" through "first" known name)
        item_one_bulk = ItemGeneralOne.Bulk()
        for (item_name, known_names) in [['one_more', ['first', 'one_more',]],
                                         ['three', ['third', 'three']]]:
            item_one = item_one_bulk.gen(f_string=item_name)
            for known_name in known_names:
                item_one['two_1_x'].gen(f_string=known_name)
            
        persister.persist(item_one_bulk)
        
        # updating two models (testing mathing x-to-many)
        item_one_bulk = ItemGeneralOne.Bulk()
        for (item_name, known_names) in [['two_more', ['second', 'two',
                                                       'two_more',]],
                                         ['three_more', ['third', 'three',
                                                         'three_more']]]:
            item_one = item_one_bulk.gen(f_string=item_name)
            for known_name in known_names:
                item_one['two_1_x'].gen(f_string=known_name)
        
        persister.persist(item_one_bulk)
        
        # checking the models
        sort_func = lambda model: model.f_string
        models_one = self.get_all_models(self.ModelGeneralOne,
                                         sort_key=sort_func)
        self.assertEqual(len(models_one), 3)
        
        expected = [['one_more', ['first', 'one', 'one_more']],
                    ['two_more', ['second', 'two', 'two_more']],
                    ['three_more', ['third', 'three', 'three_more']]]
        expected.sort(key=lambda entry: entry[0])
        
        for i, (expected_name, expected_known_names) in enumerate(expected):
            
            model_one = models_one[i]
            self.assertEqual(model_one.f_string, expected_name)
            
            models_two = self.get_related_x_to_many(model_one, 'two_1_x',
                                                    sort_func)
            actual_known_names = [model_two.f_string
                                  for model_two in models_two]
            known_names.sort()
            self.assertEqual(actual_known_names, expected_known_names)

    
    def test_persist_bulk_item(self):
        class ItemGeneralOne(Item):
            allow_merge_items = True
            model_cls = self.ModelGeneralOne
            creators = [{'f_integer'}]
            getters = [{'f_integer'}, {'f_float'}]
        
        class ItemGeneralTwo(Item):
            allow_merge_items = True
            model_cls = self.ModelGeneralTwo
            creators = [{'f_integer'}]
            getters = [{'f_integer'}, {'f_float'}]
        
        adapter_cls = get_adapter_cls(self.ModelGeneralOne)
        persister = self.persister
        
        # generating 10 simple items
        bulk_one = ItemGeneralOne.Bulk()
        for i in range(10):
            bulk_one.gen(id=i, f_integer=i+100, f_float=i+1000)
        
        previous_bulk = bulk_one.bulk[:]
        items, model_lists = persister.persist(bulk_one)
        self.assertEqual(bulk_one.bulk, previous_bulk,
                         'Bulk was not changed after persistence')
        
        self.assertEqual(len(items), 10)
        self.assertEqual(len(items), len(model_lists))
        models = [model_entries[0] for model_entries in model_lists
                  if self.assertEqual(len(model_entries), 1) is None]
        models.sort(key=lambda model: model.id)
        loaded_models = self.get_all_models(self.ModelGeneralOne)
        self.assertEqual(len(models), 10)
        for i, model in enumerate(models):
            self.assertIn(model, loaded_models)
            self.assertEqual(model.id, i)
            self.assertEqual(model.f_integer, i+100)
            self.assertEqual(model.f_float, i+1000)
            self.assertIs(model.f_boolean, None)  # for future tests
        
        # generating 10 items that has previous 5 and new 5 items as relations
        bulk_two = ItemGeneralTwo.Bulk()
        for i in range(10):
            item = bulk_two.gen(id=i, f_integer=i+200, f_float=i+2000)
            if i < 5:
                # last five item ones will have twos with IDs from 0 to 4
                # (all `i` values), item twos from 5 to 9
                item['one_x_x'] = bulk_one.slice(start=5)
                item['one_x_x__f_boolean'] = 'true'
                
                if i == 1:
                    # items are from previously saved bulk
                    # item one at index zero has ID = 0,
                    # item two has ID = 1 (current `i`, current item)
                    item['one_1_1'] = items[0]
                    item['one_1_x'].add(items[0])
            else:
                for j in range(5, 10):
                    # generated items are the same for all iterations,
                    # item twos from 5 to 9 will have item ones with IDs
                    # from 600 to 604, item ones on the other side will have
                    # item twos with IDs from 5 to 9 (all `i` values)
                    item['one_x_x'].gen(id=j+600-5, f_integer=j+200-5,
                                        f_float=j+2000-5)
        
        items, model_lists = persister.persist(bulk_two)
        self.assertEqual(len(items), 10)
        self.assertEqual(len(items), len(model_lists))
        models = [model_entries[0] for model_entries in model_lists
                  if self.assertEqual(len(model_entries), 1) is None]
        
        # checking item twos ---------------------------------------------------
        
        # 5 items were not changed, 5 items were updated, 5 items were created
        all_models = self.get_all_models(self.ModelGeneralOne)
        all_models.sort(key=lambda model: model.id)
        self.assertEqual(len(all_models), 15)
        
        # checking fields (using IDs for relations)
        expected_values = [
            # first 5 items that were not changed
            dict(id=0, f_integer=100, f_float=1000.0, f_boolean=None,
                 two_1_1=1, two_x_1=1),
            dict(id=1, f_integer=101, f_float=1001.0, f_boolean=None),
            dict(id=2, f_integer=102, f_float=1002.0, f_boolean=None),
            dict(id=3, f_integer=103, f_float=1003.0, f_boolean=None),
            dict(id=4, f_integer=104, f_float=1004.0, f_boolean=None),
            # 5 items that were updated
            dict(id=5, f_integer=105, f_float=1005.0, f_boolean=True,
                 two_x_x=[0,1,2,3,4]),
            dict(id=6, f_integer=106, f_float=1006.0, f_boolean=True,
                 two_x_x=[0,1,2,3,4]),
            dict(id=7, f_integer=107, f_float=1007.0, f_boolean=True,
                 two_x_x=[0,1,2,3,4]),
            dict(id=8, f_integer=108, f_float=1008.0, f_boolean=True,
                 two_x_x=[0,1,2,3,4]),
            dict(id=9, f_integer=109, f_float=1009.0, f_boolean=True,
                 two_x_x=[0,1,2,3,4]),
            # 5 items that were created
            dict(id=600, f_integer=200, f_float=2000.0, f_boolean=None,
                 two_x_x=[5,6,7,8,9]),
            dict(id=601, f_integer=201, f_float=2001.0, f_boolean=None,
                 two_x_x=[5,6,7,8,9]),
            dict(id=602, f_integer=202, f_float=2002.0, f_boolean=None,
                 two_x_x=[5,6,7,8,9]),
            dict(id=603, f_integer=203, f_float=2003.0, f_boolean=None,
                 two_x_x=[5,6,7,8,9]),
            dict(id=604, f_integer=204, f_float=2004.0, f_boolean=None,
                 two_x_x=[5,6,7,8,9]),
        ]
        relations = {
            fname: direction
            for fname, _, direction, _ in persister.adapter_cls.iter_relations(
                all_models[0].__class__)
        }
        for i, (expected, model) in enumerate(zip(expected_values, all_models)):
            for key, value in expected.items():
                if key not in relations:
                    model_value = getattr(model, key)
                    err_msg = '{}: {} = {}'.format(i, key, model_value)
                    if key != 'f_boolean':
                        self.assertEqual(model_value, value, err_msg)
                    else:
                        self.assertIs(model_value, value, err_msg)
                else:
                    if relations[key].is_x_to_many():
                        model_value = adapter_cls.get_related_x_to_many(
                            model, key)
                        ids = list(m.id for m in model_value)
                        ids.sort()
                        self.assertEqual(
                            ids, value,
                            '{}: {} = {}'.format(i, key, ids))
                    else:
                        model_value = getattr(model, key)
                        self.assertEqual(
                            model_value.id, value,
                            '{}: {} = {}'.format(i, key, model_value.id))
        
        # checking item ones ---------------------------------------------------
        
        # 10 items were created, other creations or no changes were made
        # (5 items were reused, 5 items were created)
        all_models = self.get_all_models(self.ModelGeneralTwo)
        all_models.sort(key=lambda model: model.id)
        self.assertEqual(len(all_models), 10)
        
        expected_values = [
            dict(id=0, f_integer=200, f_float=2000.0,
                 one_x_x=[5,6,7,8,9]),
            dict(id=1, f_integer=201, f_float=2001.0,
                 one_x_x=[5,6,7,8,9],
                 one_1_1=0, one_1_x=[0]),
            dict(id=2, f_integer=202, f_float=2002.0,
                 one_x_x=[5,6,7,8,9]),
            dict(id=3, f_integer=203, f_float=2003.0,
                 one_x_x=[5,6,7,8,9]),
            dict(id=4, f_integer=204, f_float=2004.0,
                 one_x_x=[5,6,7,8,9]),
            
            dict(id=5, f_integer=205, f_float=2005.0,
                 one_x_x=[600,601,602,603,604]),
            dict(id=6, f_integer=206, f_float=2006.0,
                 one_x_x=[600,601,602,603,604]),
            dict(id=7, f_integer=207, f_float=2007.0,
                 one_x_x=[600,601,602,603,604]),
            dict(id=8, f_integer=208, f_float=2008.0,
                 one_x_x=[600,601,602,603,604]),
            dict(id=9, f_integer=209, f_float=2009.0,
                 one_x_x=[600,601,602,603,604]),
        ]
        relations = {
            fname: direction
            for fname, _, direction, _ in persister.adapter_cls.iter_relations(
                all_models[0].__class__)
        }
        for i, (expected, model) in enumerate(zip(expected_values, all_models)):
            for key, value in expected.items():
                if key not in relations:
                    model_value = getattr(model, key)
                    err_msg = '{}: {} = {}'.format(i, key, model_value)
                    self.assertEqual(model_value, value, err_msg)
                else:
                    if relations[key].is_x_to_many():
                        model_value = adapter_cls.get_related_x_to_many(
                            model, key)
                        ids = list(m.id for m in model_value)
                        ids.sort()
                        self.assertEqual(
                            ids, value,
                            '{}: {} = {}'.format(i, key, ids))
                    else:
                        model_value = getattr(model, key)
                        self.assertEqual(
                            model_value.id, value,
                            '{}: {} = {}'.format(i, key, model_value.id))
                        
    
    def test_persist_single_item_with_bulk_related(self):
        class ItemGeneralOne(Item):
            model_cls = self.ModelGeneralOne
            creators = [{'id'}]
            getters = [{'id'}]
        
        class ItemGeneralTwo(Item):
            model_cls = self.ModelGeneralTwo
            creators = [{'id'}]
            getters = [{'id'}]
        
        adapter_cls = get_adapter_cls(self.ModelGeneralOne)
        persister = self.persister
        
        item_one = ItemGeneralOne(id='5', f_float='50.50')
        item_one(two_1_1=ItemGeneralTwo(id='10', f_string='1-to-1'),
                 two_x_1=ItemGeneralTwo(id='20', f_string='X-to-1'))
        bulk = item_one['two_1_x']
        bulk.gen(id='30', f_string='1-to-x first')
        bulk.gen(id='40', f_string='1-to-x second')
        bulk = item_one['two_x_x']
        bulk.gen(id='50', f_string='x-to-x first')
        bulk.gen(id='60', f_string='x-to-x second')
        
        items, model_lists = persister.persist(item_one)
        
        self.assertEqual(len(items), 1)
        self.assertEqual(len(items), len(model_lists))
        models = model_lists[0]
        self.assertEqual(len(models), 1)
        self.assertIs(items[0], item_one)
        
        # checking model data
        model = models[0]
        self.assertEqual(model.id, 5)
        self.assertEqual(model.f_float, 50.5)
        
        self.assertIsNotNone(model.two_1_1)
        self.assertEqual(model.two_1_1.id, 10)
        self.assertEqual(model.two_1_1.f_string, '1-to-1')
        
        two_1_x = adapter_cls.get_related_x_to_many(model, 'two_1_x')
        two_1_x.sort(key=lambda model: model.id)
        self.assertEqual(len(two_1_x), 2)
        self.assertEqual(two_1_x[0].id, 30)
        self.assertEqual(two_1_x[0].f_string, '1-to-x first')
        self.assertEqual(two_1_x[1].id, 40)
        self.assertEqual(two_1_x[1].f_string, '1-to-x second')
        
        two_x_x = adapter_cls.get_related_x_to_many(model, 'two_x_x')
        two_x_x.sort(key=lambda model: model.id)
        self.assertEqual(len(two_x_x), 2)
        self.assertEqual(two_x_x[0].id, 50)
        self.assertEqual(two_x_x[0].f_string, 'x-to-x first')
        self.assertEqual(two_x_x[1].id, 60)
        self.assertEqual(two_x_x[1].f_string, 'x-to-x second')
        
    
    def test_update_only_mode(self):
        class ItemGeneralOne(Item):
            model_cls = self.ModelGeneralOne
            creators = [{'f_integer'}]
            getters = [{'f_integer'}]
            update_only_mode = True
        
        self.item_cls_manager.autogenerate = True
        persister = self.persister
        
        bulk_one = ItemGeneralOne.Bulk()
        item = bulk_one.gen(f_integer='10', f_text='10-first')
        item.update_only_mode = False
        item = bulk_one.gen(f_integer='20', f_text='20-first')
        item.update_only_mode = False
        
        items, _ = persister.persist(bulk_one)
        self.assertEqual(len(items), 2)
        
        sort_func = lambda model: model.f_integer
        
        models_one = self.get_all_models(self.ModelGeneralOne,
                                         sort_key=sort_func)
        self.assertEqual(len(models_one), 2)
        self.assertEqual(models_one[0].f_integer, 10)
        self.assertEqual(models_one[0].f_text, '10-first')
        self.assertEqual(models_one[1].f_integer, 20)
        self.assertEqual(models_one[1].f_text, '20-first')
        
        bulk_one = ItemGeneralOne.Bulk()
        item = bulk_one.gen(f_integer='10', f_text='10-second')
        item = bulk_one.gen(f_integer='30', f_text='30-second')
        
        items, _ = persister.persist(bulk_one)
        self.assertEqual(len(items), 1)
        models_one = self.get_all_models(self.ModelGeneralOne,
                                         sort_key=sort_func)
        self.assertEqual(len(models_one), 2)
        self.assertEqual(models_one[0].f_integer, 10)
        self.assertEqual(models_one[0].f_text, '10-second')
        self.assertEqual(models_one[1].f_integer, 20)
        self.assertEqual(models_one[1].f_text, '20-first')
        
    
    def test_norewrite_fields(self):
        
        class ItemGeneralOne(Item):
            model_cls = self.ModelGeneralOne
            creators = [{'f_integer'}]
            getters = [{'f_integer'}]
            norewrite_fields = {
                'f_text': True,
                'f_string': False,
            }
         
        class ItemGeneralTwo(Item):
            model_cls = self.ModelGeneralTwo
            creators = [{'f_integer'}]
            getters = [{'f_integer'}]
            

        persister = self.persister
         
        #--- normal fields ---
        # all fields set
        item_one = ItemGeneralOne(f_integer=1,
                                  f_text='text-1',
                                  f_string='string-1',
                                  f_float=1.0)
        _, model_ones_list = persister.persist(item_one)
        self.assertEqual(len(model_ones_list), 1)
        self.assertEqual(len(model_ones_list[0]), 1)
        model_one = model_ones_list[0][0]
          
        # model did not exist, everything was set
        self.assertEqual(model_one.f_integer, 1)
        self.assertEqual(model_one.f_text, 'text-1')
        self.assertEqual(model_one.f_string, 'string-1')
        self.assertEqual(model_one.f_float, 1.0)
          
        item_one = ItemGeneralOne(f_integer=1,
                                  f_text='text-2',
                                  f_string='string-2',
                                  f_float=2.0)
        _, model_ones_list = persister.persist(item_one)
        self.assertEqual(len(model_ones_list), 1)
        self.assertEqual(len(model_ones_list[0]), 1)
        model_one = model_ones_list[0][0]
          
        # only field that can be rewritten changed
        self.assertEqual(model_one.f_integer, 1)
        self.assertEqual(model_one.f_text, 'text-1')
        self.assertEqual(model_one.f_string, 'string-1')
        self.assertEqual(model_one.f_float, 2.0)  # changed
          
        # model did not exist, fields from norewrite are not set
        item_one = ItemGeneralOne(f_integer=2,
                                  f_float=2.0)
        _, model_ones_list = persister.persist(item_one)
        self.assertEqual(len(model_ones_list), 1)
        self.assertEqual(len(model_ones_list[0]), 1)
        model_one = model_ones_list[0][0]
         
        # model did not exist, everything that item had was set
        self.assertEqual(model_one.f_integer, 2)
        self.assertEqual(model_one.f_text, None)
        self.assertEqual(model_one.f_string, None)
        self.assertEqual(model_one.f_float, 2.0)
         
        item_one = ItemGeneralOne(f_integer=2,
                                  f_text='text-2',
                                  f_string='string-2',
                                  f_float=3.0)
        _, model_ones_list = persister.persist(item_one)
        self.assertEqual(len(model_ones_list), 1)
        self.assertEqual(len(model_ones_list[0]), 1)
        model_one = model_ones_list[0][0]
         
        # only field that can be rewritten changed
        self.assertEqual(model_one.f_integer, 2)
        self.assertEqual(model_one.f_text, 'text-2')
        self.assertEqual(model_one.f_string, None)  # cannot overwrite
        self.assertEqual(model_one.f_float, 3.0)  # changed
        
        
    def test_norewrite_relations_true(self):
        
        class ItemGeneralOne(Item):
            model_cls = self.ModelGeneralOne
            creators = [{'f_integer'}]
            getters = [{'f_integer'}]
            norewrite_fields = {
                'two_1_1': True,
                'two_1_x': True,
                'two_x_1': True,
                'two_x_x': True,
                
            }
         
        class ItemGeneralTwo(Item):
            model_cls = self.ModelGeneralTwo
            creators = [{'f_integer'}]
            getters = [{'f_integer'}]
        
        persister = self.persister
        sort_func = lambda model: model.f_integer
        
        item_one = ItemGeneralOne(f_integer=1)
        persister.persist(item_one)
        model_ones = self.get_all_models(self.ModelGeneralOne, sort_func)
        self.assertEqual(len(model_ones), 1)
        self.assertEqual(model_ones[0].f_integer, 1)
        
        #--- all newly created that can rewrite none ---
        item_one = ItemGeneralOne(
            f_integer=1,
            two_1_1=ItemGeneralTwo(f_integer=2),
            two_1_x=[ItemGeneralTwo(f_integer=3),
                     ItemGeneralTwo(f_integer=4)],
            two_x_1=ItemGeneralTwo(f_integer=5),
            two_x_x=[ItemGeneralTwo(f_integer=6),
                     ItemGeneralTwo(f_integer=7)],
        )
        _, models_list = persister.persist(item_one)
        self.assertEqual(len(models_list), 1)
        self.assertEqual(len(models_list[0]), 1)
        model_one = models_list[0][0]
        
        two_1_x = self.get_related_x_to_many(model_one, 'two_1_x', sort_func)
        two_x_x = self.get_related_x_to_many(model_one, 'two_x_x', sort_func)
        self.assertEqual(len(two_1_x), 2)
        self.assertEqual(len(two_x_x), 2)
        
        self.assertEqual(model_one.f_integer, 1)
        self.assertEqual(model_one.two_1_1.f_integer, 2)
        self.assertEqual(two_1_x[0].f_integer, 3)
        self.assertEqual(two_1_x[1].f_integer, 4)
        self.assertEqual(model_one.two_x_1.f_integer, 5)
        self.assertEqual(two_x_x[0].f_integer, 6)
        self.assertEqual(two_x_x[1].f_integer, 7)
        
        #--- item_one already exists and has values set, ---
        #--- nothing must be rewritten                   ---  
        item_one = ItemGeneralOne(
            f_integer=1,
            two_1_1=ItemGeneralTwo(f_integer=1002),
            two_1_x=[ItemGeneralTwo(f_integer=1003),
                     ItemGeneralTwo(f_integer=1004)],
            two_x_1=ItemGeneralTwo(f_integer=1005),
            two_x_x=[ItemGeneralTwo(f_integer=1006),
                     ItemGeneralTwo(f_integer=1007)]
        )
        _, models_list = persister.persist(item_one)
        self.assertEqual(len(models_list), 1)
        self.assertEqual(len(models_list[0]), 1)
        model_one = models_list[0][0]
        
        # nothing changed
        two_1_x = self.get_related_x_to_many(model_one, 'two_1_x', sort_func)
        two_x_x = self.get_related_x_to_many(model_one, 'two_x_x', sort_func)
        self.assertEqual(len(two_1_x), 2)
        self.assertEqual(len(two_x_x), 2)
        
        self.assertEqual(model_one.f_integer, 1)
        self.assertEqual(model_one.two_1_1.f_integer, 2)
        self.assertEqual(two_1_x[0].f_integer, 3)
        self.assertEqual(two_1_x[1].f_integer, 4)
        self.assertEqual(model_one.two_x_1.f_integer, 5)
        self.assertEqual(two_x_x[0].f_integer, 6)
        self.assertEqual(two_x_x[1].f_integer, 7)
        
        #--- checking for the other side ---
        item_two = ItemGeneralTwo(f_integer=1000000)
        persister.persist(item_two)
        model_twos = self.get_all_models(self.ModelGeneralTwo, sort_func)
        self.assertEqual(model_twos[-1].f_integer, 1000000)
        
        model_ones = self.get_all_models(self.ModelGeneralOne, sort_func)
        # model one with `f_integer=1000000` does not exists
        self.assertLess(model_ones[-1].f_integer, 1000000)
        # model_two can be rewritten
        item_one = ItemGeneralOne(
            f_integer=1000000,
            two_1_1=item_two,
            two_1_x=[item_two],
            two_x_1=item_two,
            two_x_x=[item_two]
        )
        _, models_list = persister.persist(item_one)
        self.assertEqual(len(models_list), 1)
        self.assertEqual(len(models_list[0]), 1)
        model_one = models_list[0][0]
        
        two_1_x = self.get_related_x_to_many(model_one, 'two_1_x', sort_func)
        two_x_x = self.get_related_x_to_many(model_one, 'two_x_x', sort_func)
        self.assertEqual(len(two_1_x), 1)
        self.assertEqual(len(two_x_x), 1)
        
        self.assertEqual(model_one.f_integer, 1000000)
        self.assertEqual(model_one.two_1_1.f_integer, 1000000)
        self.assertEqual(two_1_x[0].f_integer, 1000000)
        self.assertEqual(model_one.two_x_1.f_integer, 1000000)
        self.assertEqual(two_x_x[0].f_integer, 1000000)
        
        #--- no rewrite for model_two ---
        model_ones = self.get_all_models(self.ModelGeneralOne, sort_func)
        # model one with `f_integer=2000000` does not exists
        self.assertLess(model_ones[-1].f_integer, 2000000)
        # model_two cannot be rewritten
        item_one = ItemGeneralOne(
            f_integer=2000000,
            two_1_1=item_two,
            two_1_x=[item_two],
            two_x_1=item_two,
            two_x_x=[item_two]
        )
        _, models_list = persister.persist(item_one)
        self.assertEqual(len(models_list), 1)
        self.assertEqual(len(models_list[0]), 1)
        model_one = models_list[0][0]
        
        two_1_x = self.get_related_x_to_many(model_one, 'two_1_x', sort_func)
        two_x_x = self.get_related_x_to_many(model_one, 'two_x_x', sort_func)
        self.assertEqual(len(two_1_x), 0)
        self.assertEqual(len(two_x_x), 0)
        
        self.assertEqual(model_one.f_integer, 2000000)
        self.assertTrue(not hasattr(model_one, 'two_1_1') or
                        model_one.two_1_1 is None)
        self.assertTrue(not hasattr(model_one, 'two_x_1') or
                        model_one.two_x_1 is None)
        
    
    def test_norewrite_relations_false(self):
        
        class ItemGeneralOne(Item):
            model_cls = self.ModelGeneralOne
            creators = [{'f_integer'}]
            getters = [{'f_integer'}]
            norewrite_fields = {
                'two_1_1': False,
                'two_1_x': False,
                'two_x_1': False,
                'two_x_x': False,
                
            }
         
        class ItemGeneralTwo(Item):
            model_cls = self.ModelGeneralTwo
            creators = [{'f_integer'}]
            getters = [{'f_integer'}]
        
        persister = self.persister
        sort_func = lambda model: model.f_integer
        
        item_one = ItemGeneralOne(f_integer=1)
        persister.persist(item_one)
        model_ones = self.get_all_models(self.ModelGeneralOne, sort_func)
        self.assertEqual(len(model_ones), 1)
        self.assertEqual(model_ones[0].f_integer, 1)
        
        #--- all newly created that but cannot rewrite none ---
        item_one = ItemGeneralOne(
            f_integer=1,
            two_1_1=ItemGeneralTwo(f_integer=2),
            two_1_x=[ItemGeneralTwo(f_integer=3),
                     ItemGeneralTwo(f_integer=4)],
            two_x_1=ItemGeneralTwo(f_integer=5),
            two_x_x=[ItemGeneralTwo(f_integer=6),
                     ItemGeneralTwo(f_integer=7)],
        )
        _, models_list = persister.persist(item_one)
        self.assertEqual(len(models_list), 1)
        self.assertEqual(len(models_list[0]), 1)
        model_one = models_list[0][0]
        
        # no related models
        two_1_x = self.get_related_x_to_many(model_one, 'two_1_x', sort_func)
        two_x_x = self.get_related_x_to_many(model_one, 'two_x_x', sort_func)
        self.assertEqual(len(two_1_x), 0)
        self.assertEqual(len(two_x_x), 0)
        
        self.assertEqual(model_one.f_integer, 1)
        self.assertTrue(not hasattr(model_one, 'two_1_1') or
                        model_one.two_1_1 is None)
        self.assertTrue(not hasattr(model_one, 'two_x_1') or
                        model_one.two_x_1 is None)
        
        # but the other models were created
        models_two = self.get_all_models(self.ModelGeneralTwo, sort_func)
        expected_f_integers = [2, 3, 4, 5, 6, 7]
        f_integers = [model.f_integer for model in models_two]
        self.assertEqual(f_integers, expected_f_integers)
        
        #--- all newly created, even model_one ---
        item_one = ItemGeneralOne(
            f_integer=2,
            two_1_1=ItemGeneralTwo(f_integer=1002),
            two_1_x=[ItemGeneralTwo(f_integer=1003),
                     ItemGeneralTwo(f_integer=1004)],
            two_x_1=ItemGeneralTwo(f_integer=1005),
            two_x_x=[ItemGeneralTwo(f_integer=1006),
                     ItemGeneralTwo(f_integer=1007)],
        )
        _, models_list = persister.persist(item_one)
        self.assertEqual(len(models_list), 1)
        self.assertEqual(len(models_list[0]), 1)
        model_one = models_list[0][0]
        
        # relations were set
        two_1_x = self.get_related_x_to_many(model_one, 'two_1_x', sort_func)
        two_x_x = self.get_related_x_to_many(model_one, 'two_x_x', sort_func)
        self.assertEqual(len(two_1_x), 2)
        self.assertEqual(len(two_x_x), 2)
        
        self.assertEqual(model_one.f_integer, 2)
        self.assertEqual(model_one.two_1_1.f_integer, 1002)
        self.assertEqual(two_1_x[0].f_integer, 1003)
        self.assertEqual(two_1_x[1].f_integer, 1004)
        self.assertEqual(model_one.two_x_1.f_integer, 1005)
        self.assertEqual(two_x_x[0].f_integer, 1006)
        self.assertEqual(two_x_x[1].f_integer, 1007)
        
        #--- checking for the other side ---
        item_two = ItemGeneralTwo(f_integer=1000000)
        persister.persist(item_two)
        model_twos = self.get_all_models(self.ModelGeneralTwo, sort_func)
        self.assertEqual(model_twos[-1].f_integer, 1000000)
        
        model_ones = self.get_all_models(self.ModelGeneralOne, sort_func)
        # model one with `f_integer=1000000` does not exists
        self.assertLess(model_ones[-1].f_integer, 1000000)
        # model_two cannot be rewritten
        item_one = ItemGeneralOne(
            f_integer=1000000,
            two_1_1=item_two,
            two_1_x=[item_two],
            two_x_1=item_two,
            two_x_x=[item_two]
        )
        _, models_list = persister.persist(item_one)
        self.assertEqual(len(models_list), 1)
        self.assertEqual(len(models_list[0]), 1)
        model_one = models_list[0][0]
        
        two_1_x = self.get_related_x_to_many(model_one, 'two_1_x', sort_func)
        two_x_x = self.get_related_x_to_many(model_one, 'two_x_x', sort_func)
        self.assertEqual(len(two_1_x), 0)
        self.assertEqual(len(two_x_x), 0)
        
        self.assertEqual(model_one.f_integer, 1000000)
        self.assertTrue(not hasattr(model_one, 'two_1_1') or
                        model_one.two_1_1 is None)
        self.assertTrue(not hasattr(model_one, 'two_x_1') or
                        model_one.two_x_1 is None)
    
    
    def test_norewrite_nullables(self):
        class ItemGeneralOne(Item):
            model_cls = self.ModelGeneralOne
            creators = [{'f_integer'}]
            getters = [{'f_integer'}]
            norewrite_fields = {
                'two_1_1': True,
                'two_x_x': True,
            }
            nullables = ['f_text', 'two_1_1', 'two_x_x']
            relations = {
                'two_x_x': {
                    'replace_x_to_many': True,
                }
            }
         
        class ItemGeneralTwo(Item):
            model_cls = self.ModelGeneralTwo
            creators = [{'f_integer'}]
            getters = [{'f_integer'}]
            nullables = ['f_text', 'one_1_1', 'one_x_x']
            relations = {
                'one_x_x': {
                    'replace_x_to_many': True,
                }
            }
        
        persister = self.persister
        
        item_one = ItemGeneralOne(
            f_integer=1,
            f_text='text',
            two_1_1=ItemGeneralTwo(f_integer=2),
            two_x_x=[ItemGeneralTwo(f_integer=3)]
        )
        _, model_lists = persister.persist(item_one)
        self.assertEqual(len(model_lists), 1)
        self.assertEqual(len(model_lists[0]), 1)
        model_one = model_lists[0][0]
        self.assertEqual(model_one.f_integer, 1)
        self.assertEqual(model_one.f_text, 'text')
        self.assertEqual(model_one.two_1_1.f_integer, 2)
        two_x_x = self.get_related_x_to_many(model_one, 'two_x_x')
        self.assertEqual(len(two_x_x), 1)
        self.assertEqual(two_x_x[0].f_integer, 3)
        
        # not all fields must not be rewritten with `None`
        item_one = ItemGeneralOne(f_integer=1)
        persister.persist(item_one)
        model_ones = self.get_all_models(self.ModelGeneralOne)
        self.assertEqual(len(model_ones), 1)
        
        model_one = model_ones[0]
        self.assertEqual(model_one.f_integer, 1)
        self.assertEqual(model_one.f_text, None)  # rewritten
        self.assertEqual(model_one.two_1_1.f_integer, 2)
        two_x_x = self.get_related_x_to_many(model_one, 'two_x_x')
        self.assertEqual(len(two_x_x), 1)
        self.assertEqual(two_x_x[0].f_integer, 3)
    
    
    def test_norewrite_cannot_create_1_to_1(self):
        class ItemGeneralOne(Item):
            model_cls = self.ModelGeneralOne
            creators = [{'f_integer'}]
            getters = [{'f_integer'}]
            norewrite_fields = {
                'two_1_1': False,
            }
         
        class ItemGeneralTwo(Item):
            model_cls = self.ModelGeneralTwo
            creators = [{'f_integer', 'one_1_1'}]
            getters = [{'f_integer'}]
            
        persister = self.persister
        
        item_one = ItemGeneralOne(f_integer=1)
        persister.persist(item_one)
        
        # item ones' two_1_1 cannot be ovewritten, hence `item_two` cannot
        # be created
        item_two = ItemGeneralTwo(
            f_integer=2,
            one_1_1=item_one
        )
        _, model_lists = persister.persist(item_two)
        self.assertEqual(len(model_lists), 0)
        
        model_twos = self.get_all_models(self.ModelGeneralTwo)
        self.assertEqual(len(model_twos), 0)
        
        model_ones = self.get_all_models(self.ModelGeneralOne)
        self.assertEqual(len(model_ones), 1)
        model_one = model_ones[0]
        self.assertEqual(model_one.f_integer, 1)
        self.assertTrue(not hasattr(model_one, 'one_1_1') or
                        model_one.one_1_1 is None)
    
    
    def test_norewrite_cannot_create_1_to_x(self):
        class ItemGeneralOne(Item):
            model_cls = self.ModelGeneralOne
            creators = [{'f_integer'}]
            getters = [{'f_integer'}]
            norewrite_fields = {
                'two_1_x': False,
            }
         
        class ItemGeneralTwo(Item):
            model_cls = self.ModelGeneralTwo
            creators = [{'f_integer', 'one_x_1'}]
            getters = [{'f_integer'}]
        
        persister = self.persister
        sort_func = lambda model: model.f_integer
        
        # both items are created
        item_one = ItemGeneralOne(f_integer=10)
        for i in range(2):
            item_one['two_1_x'].gen(f_integer=20+i)
        persister.persist(item_one)
        
        model_ones = self.get_all_models(self.ModelGeneralOne,
                                         sort_key=sort_func)
        self.assertEqual(len(model_ones), 1)
        model_one = model_ones[0]
        self.assertEqual(model_one.f_integer, 10)
        two_1_x = self.get_related_x_to_many(model_one, 'two_1_x',
                                            sort_key=sort_func)
        self.assertEqual(len(two_1_x), 2)
        self.assertEqual(two_1_x[0].f_integer, 20)
        self.assertEqual(two_1_x[1].f_integer, 21)
        
        # one item cannot be created (cannot overwrite in ModelGeneralOne)
        item_one = ItemGeneralOne(f_integer=10)
        for i in range(1, 3):
            item_one['two_1_x'].gen(f_integer=20+i, f_float=20+i + i/10)
        persister.persist(item_one)
        
        model_ones = self.get_all_models(self.ModelGeneralOne,
                                         sort_key=sort_func)
        self.assertEqual(len(model_ones), 1)
        model_one = model_ones[0]
        self.assertEqual(model_one.f_integer, 10)
        two_1_x = self.get_related_x_to_many(model_one, 'two_1_x',
                                            sort_key=sort_func)
        self.assertEqual(len(two_1_x), 2)
        self.assertEqual(two_1_x[0].f_integer, 20)
        self.assertIsNone(two_1_x[0].f_float)
        self.assertEqual(two_1_x[1].f_integer, 21)
        self.assertEqual(two_1_x[1].f_float, 21.1)
        # item with `f_integer=22` must be not created
        models_two = self.get_all_models(self.ModelGeneralTwo)
        self.assertEqual(len(models_two), 2)
    
    
    def test_norewrite_none(self):
        class ItemGeneralOne(Item):
            model_cls = self.ModelGeneralOne
            creators = [{'f_integer'}]
            getters = [{'f_integer'}]
            norewrite_fields = {
                'f_string': None,
                'two_1_1': None,
                True: True,
            }
          
        class ItemGeneralTwo(Item):
            model_cls = self.ModelGeneralTwo
            creators = [{'f_integer'}]
            getters = [{'f_integer'}]
         
        persister = self.persister
         
        # creating
        item_one = ItemGeneralOne(f_integer=1,
                                  # cannot rewrite
                                  f_string='str-1',
                                  two_1_1=ItemGeneralTwo(f_integer=102),
                                  # can rewrite
                                  f_text='text-1',
                                  two_x_1=ItemGeneralTwo(f_integer=103))
        persister.persist(item_one)
        model_ones = self.get_all_models(self.ModelGeneralOne)
        self.assertEqual(len(model_ones), 1)
        model_one = model_ones[0]
        self.assertEqual(model_one.f_integer, 1)
        self.assertEqual(model_one.f_string, 'str-1')
        self.assertIsNotNone(model_one.two_1_1)
        self.assertEqual(model_one.two_1_1.f_integer, 102)
        self.assertEqual(model_one.f_text, 'text-1')
        self.assertEqual(model_one.two_x_1.f_integer, 103)
         
        # updating
        item_one = ItemGeneralOne(f_integer=1,
                                  # cannot rewrite
                                  f_string='str-2',
                                  two_1_1=ItemGeneralTwo(f_integer=202),
                                  # can rewrite
                                  f_text='text-2',
                                  two_x_1=ItemGeneralTwo(f_integer=203))

        persister.persist(item_one)
        model_ones = self.get_all_models(self.ModelGeneralOne)
        self.assertEqual(len(model_ones), 1)
        model_one = model_ones[0]
        self.assertEqual(model_one.f_integer, 1)
        self.assertEqual(model_one.f_string, 'str-2')
        self.assertIsNotNone(model_one.two_1_1)
        self.assertEqual(model_one.two_1_1.f_integer, 202)
        self.assertEqual(model_one.f_text, 'text-1')
        self.assertEqual(model_one.two_x_1.f_integer, 103)
        
    
    def test_nullables(self):
        class ItemGeneralOne(Item):
            model_cls = self.ModelGeneralOne
            creators = [{'f_integer'}]
            getters = [{'f_integer'}]
            nullables = ['f_text', 'two_1_1', 'two_x_1', 'two_x_x']
            relations = {
                'two_x_x': {
                    'replace_x_to_many': True,
                }
            }
         
        class ItemGeneralTwo(Item):
            model_cls = self.ModelGeneralTwo
            creators = [{'f_integer'}]
            getters = [{'f_integer'}]
        
        persister = self.persister
        
        item_one = ItemGeneralOne(
            f_integer=1,
            f_text='text',
            two_1_1=ItemGeneralTwo(f_integer=2),
            two_x_1=ItemGeneralTwo(f_integer=3),
            two_x_x=ItemGeneralTwo(f_integer=4),
        )
        persister.persist(item_one)
        model_ones = self.get_all_models(self.ModelGeneralOne)
        self.assertEqual(len(model_ones), 1)
        model_one = model_ones[0]
        self.assertEqual(model_one.f_integer, 1)
        self.assertEqual(model_one.f_text, 'text')
        self.assertEqual(model_one.two_1_1.f_integer, 2)
        self.assertEqual(model_one.two_x_1.f_integer, 3)
        two_x_x = self.get_related_x_to_many(model_one, 'two_x_x')
        self.assertEqual(len(two_x_x), 1)
        self.assertEqual(two_x_x[0].f_integer, 4)
        
        # rewriting nullables with other values
        item_one = ItemGeneralOne(
            f_integer=1,
            f_text='text-2',
            two_1_1=ItemGeneralTwo(f_integer=1001),
            two_x_1=ItemGeneralTwo(f_integer=1002),
            two_x_x=[ItemGeneralTwo(f_integer=1003),
                     ItemGeneralTwo(f_integer=1004)],
        )
        persister.persist(item_one)
        model_ones = self.get_all_models(self.ModelGeneralOne)
        self.assertEqual(len(model_ones), 1)
        model_one = model_ones[0]
        self.assertEqual(model_one.f_integer, 1)
        self.assertEqual(model_one.f_text, 'text-2')
        self.assertEqual(model_one.two_1_1.f_integer, 1001)
        self.assertEqual(model_one.two_x_1.f_integer, 1002)
        two_x_x = self.get_related_x_to_many(model_one, 'two_x_x')
        self.assertEqual(len(two_x_x), 2)
        self.assertEqual(two_x_x[0].f_integer, 1003)
        self.assertEqual(two_x_x[1].f_integer, 1004)
        
        # no values fo nullables
        item_one = ItemGeneralOne(f_integer=1)
        persister.persist(item_one)
        model_ones = self.get_all_models(self.ModelGeneralOne)
        self.assertEqual(len(model_ones), 1)
        model_one = model_ones[0]
        self.assertEqual(model_one.f_integer, 1)
        self.assertIsNone(model_one.f_text)
        self.assertTrue(not hasattr(model_one, 'two_1_1') or
                        model_one.two_1_1 is None)
        two_x_x = self.get_related_x_to_many(model_one, 'two_x_x')
        self.assertEqual(len(two_x_x), 0)
        
    
    def test_multiple_models_match_exception(self):
        model_one_cls = self.ModelGeneralOne
        model_two_cls = self.ModelGeneralTwo
        
        class ItemGeneralOne(Item):
            model_cls = self.ModelGeneralOne
            creators = [{'f_integer'}]
            getters = [{'f_integer'}, {'f_float', 'f_text'}]
        
        class ItemGeneralTwo(Item):
            model_cls = self.ModelGeneralTwo
            creators = [{'f_integer'}]
            getters = [{'f_integer'}, {'f_float', 'one_x_1'}]
        
        persister = self.persister
        
        # with simple fields ---------------------------------------------------
        # creating two items with different integer fields but same other fields
        item = ItemGeneralOne(f_integer='100', f_float='200.200')
        persister.persist(item)
        item = ItemGeneralOne(f_integer='200', f_float='200.200')
        persister.persist(item)
        
        # updating to get 'f_float' and 'f_text' have the same values for
        # different models 
        item = ItemGeneralOne(f_integer='100', f_text='text-1')
        persister.persist(item)
        item = ItemGeneralOne(f_integer='200', f_text='text-1')
        persister.persist(item)
        
        self.assertEqual(len(self.get_all_models(model_one_cls)), 2)
        
        # this must get two models from database
        item = ItemGeneralOne(f_integer='100',
                              f_float='200.200', f_text='text-1')
        with self.assertRaises(MultipleModelsMatch):
            persister.persist(item)
        
        # still 2 models in database
        self.assertEqual(len(self.get_all_models(model_one_cls)), 2)
        
        # using relations ------------------------------------------------------
        item = ItemGeneralTwo(f_integer='100', f_float='200.200')
        persister.persist(item)
        item = ItemGeneralTwo(f_integer='200', f_float='200.200')
        persister.persist(item)
        
        item_one = ItemGeneralOne(f_integer='300')  # new item one
        item = ItemGeneralTwo(f_integer='100', one_x_1=item_one)
        persister.persist(item)
        item = ItemGeneralTwo(f_integer='200', one_x_1=item_one)
        persister.persist(item)
        
        self.assertEqual(len(self.get_all_models(model_one_cls)), 3)
        self.assertEqual(len(self.get_all_models(model_two_cls)), 2)

        # this must get two models from database
        item = ItemGeneralTwo(f_float='200.200', one_x_1=item_one)
        with self.assertRaises(MultipleModelsMatch):
            persister.persist(item)

    
    def test_multiple_items_match_exception(self):
        
        class ItemGeneralOne(Item):
            model_cls = self.ModelGeneralOne
            creators = [{'f_integer'}]
            getters = [{'f_integer'}, {'f_float'}]
        
        class ItemGeneralTwo(Item):
            model_cls = self.ModelGeneralTwo
        
        persister = self.persister
        
        # check for existing models
        persister.persist(ItemGeneralOne(f_integer=10, f_float=1))
        persister.persist(ItemGeneralOne(f_integer=20, f_float=2))
        
        bulk = ItemGeneralOne.Bulk()
        # two items will get the same model
        bulk.gen(f_integer=10, f_string='str-value-one')
        bulk.gen(f_float=1, f_string='str-value-two')
        
        with self.assertRaises(MultipleItemsMatch):
            persister.persist(bulk)
            
        # check for newly created models
        bulk = ItemGeneralOne.Bulk()
        bulk.gen(f_integer=10, f_float=1)
        bulk.gen(f_integer=20, f_float=1)
        
        with self.assertRaises(MultipleItemsMatch):
            persister.persist(bulk)
            
    
    def test_replace_x_to_many(self):
        
        class ItemGeneralOne(Item):
            model_cls = self.ModelGeneralOne
            creators = [{'f_string'}]
            getters = [{'f_string'}]
        
        class ItemGeneralTwo(Item):
            model_cls = self.ModelGeneralTwo
            creators = [{'f_string'}]
            getters = [{'f_string'}]
            relations = {
                'one_1_x': {
                    'replace_x_to_many': True,
                }
            }
        
        adapter_cls = get_adapter_cls(self.ModelGeneralOne)
        persister = self.persister
        
        # replace_x_to_many = False
        item_one = ItemGeneralOne(f_string='1')
        item_one['two_1_x'].gen(f_string='1: 2->1')
        item_one['two_1_x'].gen(f_string='2: 2->1')
        persister.persist(item_one)
        item_one = ItemGeneralOne(f_string='1')  # item recreated
        item_one['two_1_x'].gen(f_string='3: 2->1')
        item_one['two_1_x'].gen(f_string='4: 2->1')
        
        _, model_lists = persister.persist(item_one)
        self.assertEqual(len(model_lists), 1)
        models = model_lists[0]
        self.assertEqual(len(models), 1)
        model = models[0]
        two_1_x = adapter_cls.get_related_x_to_many(model, 'two_1_x')
        self.assertEqual(len(two_1_x), 4)
        two_1_x.sort(key=lambda m: m.f_string)
        for i in range(4):
            self.assertEqual(two_1_x[i].f_string, '{}: 2->1'.format(i+1))
        
        # replace_x_to_many = True
        item_two = ItemGeneralTwo(f_string='2')
        item_two['one_1_x'].gen(f_string='1: 1->2')
        item_two['one_1_x'].gen(f_string='2: 1->2')
        persister.persist(item_two)
        item_two = ItemGeneralTwo(f_string='2')  # item recreated
        item_two['one_1_x'].gen(f_string='3: 1->2')
        item_two['one_1_x'].gen(f_string='4: 1->2')
        
        _, model_lists = persister.persist(item_two)
        self.assertEqual(len(model_lists), 1)
        models = model_lists[0]
        self.assertEqual(len(models), 1)
        model = models[0]
        one_1_x = adapter_cls.get_related_x_to_many(model, 'one_1_x')
        self.assertEqual(len(one_1_x), 2)
        
        one_1_x.sort(key=lambda m: m.f_string)
        for i in range(2):
            # `i+3` because first two items replaced
            self.assertEqual(one_1_x[i].f_string, '{}: 1->2'.format(i+3))
    
    
    def __test_replace_x_to_many_additional_refrence(self,
                                                     one_1_x_a='one_1_x_a',
                                                     two_1_x_b='two_1_x_b'):

        class ItemManyRefsOne(Item):
            model_cls = self.ModelManyRefsOne
            creators = [{'f_string'}]
            getters = [{'f_string'}]
            relations = {
                'two_1_x_b': {
                    'replace_x_to_many': True,
                },
                'two_x_x_b': {
                    'replace_x_to_many': True,
                }
            }
        
        class ItemManyRefsTwo(Item):
            model_cls = self.ModelManyRefsTwo
            creators = [{'f_string'}]
            getters = [{'f_string'}]
            relations = {
                'one_1_x_a': {
                    'replace_x_to_many': True,
                },
                'one_x_x_a': {
                    'replace_x_to_many': True,
                }
            }
        
        adapter_cls = get_adapter_cls(self.ModelManyRefsOne)
        persister = self.persister
        
        # --- creating ---
        item_two = ItemManyRefsTwo(f_string='Item 2.1')
        item_one = item_two[one_1_x_a].gen(f_string='Item 1.1')
        item_one[two_1_x_b].add(item_two)
        
        persister.persist(item_two)
        
        models_one = self.get_all_models(self.ModelManyRefsOne)
        models_two = self.get_all_models(self.ModelManyRefsTwo)
        self.assertEqual(len(models_one), 1)
        self.assertEqual(len(models_two), 1)
        self.assertEqual(models_one[0].f_string, 'Item 1.1')
        self.assertEqual(models_two[0].f_string, 'Item 2.1')
        
        x_models_two = adapter_cls.get_related_x_to_many(models_one[0],
                                                         two_1_x_b)
        x_models_one = adapter_cls.get_related_x_to_many(models_two[0],
                                                         one_1_x_a)
        self.assertEqual(len(x_models_one), 1)
        self.assertEqual(len(x_models_two), 1)
        
        self.assertEqual(x_models_one[0], models_one[0])
        self.assertEqual(x_models_two[0], models_two[0])
        
        # --- updating ---
        # item_two
        item_two = ItemManyRefsTwo(f_string='Item 2.1')
        item_two[one_1_x_a].gen(f_string='Item 1.2')
        # old item with old reference
        item_two['one_1_1_b'] = ItemManyRefsOne(f_string='Item 1.1')
        
        # item_one
        item_one = item_two['one_1_1_b']
        item_one[two_1_x_b].gen(f_string='Item 2.2')
        # old item with old reference
        item_one['two_1_1_a'] = item_two
        
        persister.persist(item_two)
        
        sort_func = lambda model: model.f_string
        
        models_one = self.get_all_models(self.ModelManyRefsOne)
        models_two = self.get_all_models(self.ModelManyRefsTwo)
        self.assertEqual(len(models_one), 2)
        self.assertEqual(len(models_two), 2)
        
        models_one.sort(key=sort_func)
        models_two.sort(key=sort_func)
        
        self.assertEqual(models_one[0].f_string, 'Item 1.1')
        self.assertEqual(models_one[1].f_string, 'Item 1.2')
        self.assertEqual(models_two[0].f_string, 'Item 2.1')
        self.assertEqual(models_two[1].f_string, 'Item 2.2')
        
        # updated relations must be without old references
        x_models_two = adapter_cls.get_related_x_to_many(models_one[0],
                                                         two_1_x_b)
        x_models_one = adapter_cls.get_related_x_to_many(models_two[0],
                                                         one_1_x_a)
        self.assertEqual(len(x_models_one), 1)
        self.assertEqual(len(x_models_two), 1)
        
        self.assertEqual(x_models_one[0], models_one[1])
        self.assertEqual(x_models_two[0], models_two[1])
        
        self.assertEqual(models_one[0].two_1_1_a, models_two[0])
        self.assertEqual(models_two[0].one_1_1_b, models_one[0])
    
    
    def test_replace_one_to_many_additional_refrence(self):
        self.__test_replace_x_to_many_additional_refrence(one_1_x_a='one_1_x_a',
                                                          two_1_x_b='two_1_x_b')
                                                     
    def test_replace_many_to_many_additional_refrence(self):
        self.__test_replace_x_to_many_additional_refrence(one_1_x_a='one_x_x_a',
                                                          two_1_x_b='two_x_x_b')
    
    def test_one_to_one_replacement(self):

        class ItemManyRefsOne(Item):
            allow_merge_items = True
            model_cls = self.ModelManyRefsOne
            creators = [{'f_string'}]
            getters = [{'f_string'}]
        
        class ItemManyRefsTwo(Item):
            allow_merge_items = True
            model_cls = self.ModelManyRefsTwo
            creators = [{'f_string'}]
            getters = [{'f_string'}]
        
        persister = self.persister
        sort_func = lambda model: model.f_string
        
        # creating
        item_two = ItemManyRefsTwo(f_string='Item 2.1')
        item_two['one_1_1_a'] = ItemManyRefsOne(f_string='Item 1.1')
         
        persister.persist(item_two)
         
        models_one = self.get_all_models(self.ModelManyRefsOne)
        models_two = self.get_all_models(self.ModelManyRefsTwo)
        self.assertEqual(len(models_one), 1)
        self.assertEqual(len(models_two), 1)
        self.assertEqual(models_two[0].f_string, 'Item 2.1')
        self.assertEqual(models_one[0].f_string, 'Item 1.1')
         
        self.assertEqual(models_two[0].one_1_1_a, models_one[0])

        # updating without pulling old item
        item_two = ItemManyRefsTwo(f_string='Item 2.1')
        item_two['one_1_1_a'] = ItemManyRefsOne(f_string='Item 1.2')
        persister.persist(item_two)
        
        models_one = self.get_all_models(self.ModelManyRefsOne, sort_func)
        models_two = self.get_all_models(self.ModelManyRefsTwo, sort_func)
        self.assertEqual(len(models_one), 2)
        self.assertEqual(len(models_two), 1)
        self.assertEqual(models_one[0].f_string, 'Item 1.1')
        self.assertEqual(models_one[0].two_1_1_a, None)
        self.assertEqual(models_one[1].f_string, 'Item 1.2')
        self.assertEqual(models_one[1].two_1_1_a, models_two[0])
        self.assertEqual(models_two[0].f_string, 'Item 2.1')
        self.assertEqual(models_two[0].one_1_1_a, models_one[1])
    
    def test_one_to_one_additional_refrence(self):

        class ItemManyRefsOne(Item):
            allow_merge_items = True
            model_cls = self.ModelManyRefsOne
            creators = [{'f_string'}]
            getters = [{'f_string'}]
        
        class ItemManyRefsTwo(Item):
            allow_merge_items = True
            model_cls = self.ModelManyRefsTwo
            creators = [{'f_string'}]
            getters = [{'f_string'}]
        
        persister = self.persister
        adapter_cls = get_adapter_cls(self.ModelManyRefsOne)
        sort_func = lambda model: model.f_string
        
        #  creating 
        item_two = ItemManyRefsTwo(f_string='Item 2.1')
        item_two['one_1_1_a'] = ItemManyRefsOne(f_string='Item 1.1')
        item_two['one_1_1_a']['two_1_1_b'] = \
            ItemManyRefsTwo(f_string='Item 2.2')
        
        persister.persist(item_two)
         
        models_one = self.get_all_models(self.ModelManyRefsOne, sort_func)
        models_two = self.get_all_models(self.ModelManyRefsTwo, sort_func)
        self.assertEqual(len(models_one), 1)
        self.assertEqual(len(models_two), 2)
        self.assertEqual(models_two[0].f_string, 'Item 2.1')
        self.assertEqual(models_one[0].f_string, 'Item 1.1')
        self.assertEqual(models_two[1].f_string, 'Item 2.2')
        
        self.assertEqual(models_one[0].two_1_1_a, models_two[0])
        self.assertEqual(models_one[0].two_1_1_b, models_two[1])
        
        #  updating with pulling old item 
        item_two = ItemManyRefsTwo(f_string='Item 2.1')
        item_two['one_1_1_a'] = ItemManyRefsOne(f_string='Item 1.2')
        item_one = item_two['one_x_x_a'].gen(f_string='Item 1.1')
        item_one['two_1_1_b'] = ItemManyRefsTwo(f_string='Item 2.3')
        # this item can potentially keep reference to item two
        item_one['two_x_x_b'].gen(f_string='Item 2.2')
          
        persister.persist(item_two)
        models_one = self.get_all_models(self.ModelManyRefsOne, sort_func)
        models_two = self.get_all_models(self.ModelManyRefsTwo, sort_func)
        self.assertEqual(len(models_one), 2)
        self.assertEqual(len(models_two), 3)
        self.assertEqual(models_two[0].f_string, 'Item 2.1')
        self.assertEqual(models_two[1].f_string, 'Item 2.2')
        self.assertEqual(models_two[2].f_string, 'Item 2.3')
        self.assertEqual(models_one[0].f_string, 'Item 1.1')
        self.assertEqual(models_one[1].f_string, 'Item 1.2')
        
        self.assertFalse(hasattr(models_one[0], 'two_1_1_a') and
                         models_one[0].two_1_1_a)
        self.assertEqual(models_one[0].two_1_1_b, models_two[2])
        
        self.assertEqual(models_two[0].one_1_1_a, models_one[1])
        self.assertFalse(hasattr(models_two[0], 'one_1_1_b') and
                         models_two[0].one_1_1_b)
        
        self.assertFalse(hasattr(models_two[1], 'one_1_1_a') and
                         models_two[1].one_1_1_a)
        self.assertFalse(hasattr(models_two[1], 'one_1_1_b') and
                         models_two[1].one_1_1_b)
        
        x_models_two = adapter_cls.get_related_x_to_many(models_one[0],
                                                         'two_x_x_b')
        self.assertEqual(len(x_models_two), 1)
        self.assertEqual(x_models_two[0].f_string, 'Item 2.2')
        
        x_models_one = adapter_cls.get_related_x_to_many(models_two[0],
                                                         'one_x_x_a')
        self.assertEqual(len(x_models_one), 1)
        self.assertEqual(x_models_one[0].f_string, 'Item 1.1')
    
    def test_multiple_model_update(self):
        model_one_cls = self.ModelGeneralOne
        model_two_cls = self.ModelGeneralTwo
        
        class ItemGeneralOne(Item):
            model_cls = self.ModelGeneralOne
            creators = [{'f_integer'}]
            getters = [{'f_integer'}, {'f_float', 'f_text'}]
        
        class ItemGeneralTwo(Item):
            model_cls = self.ModelGeneralTwo
            creators = [{'f_integer'}]
            getters = [{'f_integer'}, {'f_float', 'one_x_1'}]
        
        persister = self.persister
        
        # with simple fields ---------------------------------------------------
        # creating two items with different integer fields but same other fields
        item = ItemGeneralOne(f_integer='100', f_float='200.200',
                              f_boolean=True)
        persister.persist(item)
        item = ItemGeneralOne(f_integer='200', f_float='200.200',
                              f_boolean=False)
        persister.persist(item)
        
        # updating to get 'f_float' and 'f_text' have the same values for
        # different models 
        item = ItemGeneralOne(f_integer='100', f_text='text-1')
        persister.persist(item)
        item = ItemGeneralOne(f_integer='200', f_text='text-1')
        persister.persist(item)
        
        self.assertEqual(len(self.get_all_models(model_one_cls)), 2)
        
        # this must get two models from database
        item = ItemGeneralOne(f_integer='100',
                              f_float='200.200', f_text='text-1')
        ItemGeneralOne.allow_multi_update= True
        items, model_lists = persister.persist(item)
        ItemGeneralOne.allow_multi_update= False
        
        self.assertEqual(len(items), 1)
        self.assertEqual(len(model_lists), 1)
        self.assertEqual(len(model_lists[0]), 2)
        models = model_lists[0]
        models.sort(key=lambda model: not model.f_boolean)
        
        self.assertIs(models[0].f_boolean, True)
        self.assertEqual(models[0].f_integer, 100)
        self.assertEqual(models[0].f_float, 200.2)
        self.assertEqual(models[0].f_text, 'text-1')
        
        self.assertIs(models[1].f_boolean, False)
        self.assertEqual(models[1].f_integer, 100)
        self.assertEqual(models[1].f_float, 200.2)
        self.assertEqual(models[1].f_text, 'text-1')
        
        # still 2 models in database
        self.assertEqual(len(self.get_all_models(model_one_cls)), 2)
        
        # using relations ------------------------------------------------------
        item = ItemGeneralTwo(f_integer='100', f_float='200.200')
        persister.persist(item)
        item = ItemGeneralTwo(f_integer='200', f_float='200.200')
        persister.persist(item)
        
        item_one = ItemGeneralOne(f_integer='300')  # new item one
        item = ItemGeneralTwo(f_integer='100', one_x_1=item_one)
        persister.persist(item)
        item = ItemGeneralTwo(f_integer='200', one_x_1=item_one)
        persister.persist(item)
        
        self.assertEqual(len(self.get_all_models(model_one_cls)), 3)
        self.assertEqual(len(self.get_all_models(model_two_cls)), 2)

        # this must get two models from database
        item = ItemGeneralTwo(f_float='200.200', one_x_1=item_one)
        ItemGeneralTwo.allow_multi_update = True
        item, model_lists = persister.persist(item)
        ItemGeneralTwo.allow_multi_update = False
        
        self.assertEqual(len(items), 1)
        self.assertEqual(len(model_lists), 1)
        self.assertEqual(len(model_lists[0]), 2)
        models = model_lists[0]
        models.sort(key=lambda model: model.f_integer)
        
        self.assertEqual(models[0].f_integer, 100)
        self.assertEqual(models[0].f_float, 200.2)
        
        self.assertEqual(models[1].f_integer, 200)
        self.assertEqual(models[1].f_float, 200.2)
        
        self.assertIs(models[0].one_x_1, models[1].one_x_1)
        self.assertEqual(models[0].one_x_1.f_integer, 300)
    
    
    def test_set_multiple_related(self):
        model_one_cls = self.ModelGeneralOne
        
        class ItemGeneralOne(Item):
            allow_multi_update = True
            model_cls = self.ModelGeneralOne
            creators = [{'f_integer'}]
            getters = [{'f_integer'}, {'f_float', 'f_text'}]
        
        class ItemGeneralTwo(Item):
            allow_multi_update = True
            model_cls = self.ModelGeneralTwo
            creators = [{'f_integer'}]
            getters = [{'f_integer'}, {'f_float', 'one_x_1'}]
        
        persister = self.persister
        
        # creating two items with different integer fields but same other fields
        item = ItemGeneralOne(f_integer='100', f_float='200.200',
                              f_boolean=True)
        persister.persist(item)
        item = ItemGeneralOne(f_integer='200', f_float='200.200',
                              f_boolean=False)
        persister.persist(item)
        
        # updating to get 'f_float' and 'f_text' have the same values for
        # different models 
        item_one = ItemGeneralOne(f_integer='100', f_text='text-1')
        persister.persist(item_one)
        item_one = ItemGeneralOne(f_integer='200', f_text='text-1')
        persister.persist(item_one)
        
        self.assertEqual(len(self.get_all_models(model_one_cls)), 2)
        
        #--- set two models to x-to-many field must work -----------------------
        item_two = ItemGeneralTwo(f_integer='100')
        item_two['one_1_x'].gen(f_float='200.200', f_text='text-1')
        
        items, model_lists = persister.persist(item_two)
        self.assertEqual(len(items), 1)
        self.assertEqual(len(model_lists), 1)
        self.assertEqual(len(model_lists[0]), 1)
        
        # but the model has two related models
        one_1_x = self.get_all_models(model_one_cls)
        self.assertEqual(len(one_1_x), 2)
        
        one_1_x.sort(key=lambda model: model.f_integer)
        self.assertEqual(one_1_x[0].f_integer, 100)
        self.assertEqual(one_1_x[0].f_float, 200.2)
        self.assertEqual(one_1_x[0].f_text, 'text-1')
        self.assertEqual(one_1_x[1].f_integer, 200)
        self.assertEqual(one_1_x[1].f_float, 200.2)
        self.assertEqual(one_1_x[1].f_text, 'text-1')
        
        #--- set two models to x-to-one field must fail ------------------------
        item_two = ItemGeneralTwo(f_integer='200')
        item_two['one_1_1'](f_float='200.200', f_text='text-1')
        with self.assertRaises(MultipleModelsMatch):
            persister.persist(item_two)
        

    def test_forward_and_reverse_relations_filters_one(self):
        # referencing parent and two
        
        class ItemGeneralOne(Item):
            model_cls = self.ModelGeneralOne
            creators = [{'parent_1_1'}, {'parent_x_1'}, {'parent_x_x'},
                        {'two_1_1'}, {'two_1_x'}, {'two_x_1'}, {'two_x_x'},
                        {'f_integer'}]
            getters = [{'parent_1_1'}, {'parent_x_1'}, 
                       {'two_1_1'}, {'two_x_1'}]
        
        class ItemGeneralTwo(Item):
            model_cls = self.ModelGeneralTwo
            creators = [{'f_integer'}]
            getters = [{'f_integer'}]
            
        adapter_cls = get_adapter_cls(self.ModelGeneralOne)
        persister = self.persister
        
        # parent_1_1
        item_parent_1_1 = ItemGeneralOne(f_string='parent_1_1',
                                         f_integer='101')
        item_child_1_1 = ItemGeneralOne(f_string='child_1_1',
                                        parent_1_1=item_parent_1_1)
        persister.persist(item_child_1_1)
        models = self.get_all_models(self.ModelGeneralOne)
        model = [m for m in models if m.f_string=='child_1_1'][0]
        self.assertEqual(model.parent_1_1.f_string, 'parent_1_1')
        model = [m for m in models if m.f_string=='parent_1_1'][0]
        self.assertEqual(model.child_1_1.f_string, 'child_1_1')
        
        # parent_x_1
        item_parent_x_1 = ItemGeneralOne(f_string='parent_x_1',
                                         f_integer='901')
        item_child_1_x = ItemGeneralOne(f_string='child_1_x',
                                        parent_x_1=item_parent_x_1)
        persister.persist(item_child_1_x)
        models = self.get_all_models(self.ModelGeneralOne)
        model = [m for m in models if m.f_string=='child_1_x'][0]
        self.assertEqual(model.parent_x_1.f_string, 'parent_x_1')
        model = [m for m in models if m.f_string=='parent_x_1'][0]
        child_1_x = adapter_cls.get_related_x_to_many(model, 'child_1_x')
        self.assertEqual(len(child_1_x), 1)
        self.assertEqual(child_1_x[0].f_string, 'child_1_x')
        
        # two_1_1
        item_two_1_1 = ItemGeneralTwo(f_string='two_1_1',
                                      f_integer='101')
        item_one_1_1 = ItemGeneralOne(f_string='one_1_1',
                                      two_1_1=item_two_1_1)
        persister.persist(item_one_1_1)
        
        models = self.get_all_models(self.ModelGeneralOne)
        model = [m for m in models if m.f_string=='one_1_1'][0]
        self.assertEqual(model.two_1_1.f_string, 'two_1_1')
        models = self.get_all_models(self.ModelGeneralTwo)
        model = [m for m in models if m.f_string=='two_1_1'][0]
        self.assertEqual(model.one_1_1.f_string, 'one_1_1')
        
        # two_x_1
        item_two_x_1 = ItemGeneralTwo(f_string='two_x_1',
                                      f_integer='901')
        item_one_1_x = ItemGeneralOne(f_string='one_1_x',
                                      two_x_1=item_two_x_1)
        persister.persist(item_one_1_x)
        models = self.get_all_models(self.ModelGeneralOne)
        model = [m for m in models if m.f_string=='one_1_x'][0]
        self.assertEqual(model.two_x_1.f_string, 'two_x_1') 
        models = self.get_all_models(self.ModelGeneralTwo)
        model = [m for m in models if m.f_string=='two_x_1'][0]
        one_1_x = adapter_cls.get_related_x_to_many(model, 'one_1_x')
        self.assertEqual(len(one_1_x), 1)
        self.assertEqual(one_1_x[0].f_string, 'one_1_x')
    
    
    def test_forward_and_reverse_relations_filters_two(self):
        # referencing child and one
        
        class ItemGeneralOne(Item):
            model_cls = self.ModelGeneralOne
            creators = [{'child_1_1'}, {'child_x_x'},
                        {'f_integer'}]
            getters = [{'child_1_1'},
                       {'two_1_1'}, {'two_x_1'},
                       {'f_string'}]
        
        class ItemGeneralTwo(Item):
            model_cls = self.ModelGeneralTwo
            creators = [{'one_1_1'}, {'one_1_x'}, {'one_x_1'}, {'one_x_x'},
                        {'f_integer'}]
            getters = [{'one_1_1'}, {'one_x_1'},
                       {'f_integer'}]
        
        
        adapter_cls = get_adapter_cls(self.ModelGeneralOne)
        persister = self.persister
        
        # child_1_1
        item_child_1_1 = ItemGeneralOne(f_string='child_1_1',
                                        f_integer='101')
        item_parent_1_1 = ItemGeneralOne(f_string='parent_1_1',
                                         child_1_1=item_child_1_1)
        persister.persist(item_parent_1_1)
        models = self.get_all_models(self.ModelGeneralOne)
        model = [m for m in models if m.f_string=='parent_1_1'][0]
        self.assertEqual(model.child_1_1.f_string, 'child_1_1')
        model = [m for m in models if m.f_string=='child_1_1'][0]
        self.assertEqual(model.parent_1_1.f_string, 'parent_1_1')
        
        # one_1_1
        item_one_1_1 = ItemGeneralOne(f_string='one_1_1',
                                      f_integer='1101')
        item_two_1_1 = ItemGeneralTwo(f_string='two_1_1',
                                      one_1_1=item_one_1_1)
        persister.persist(item_two_1_1)
        models = self.get_all_models(self.ModelGeneralTwo)
        model = [m for m in models if m.f_string=='two_1_1'][0]
        self.assertEqual(model.one_1_1.f_string, 'one_1_1')
        models = self.get_all_models(self.ModelGeneralOne)
        model = [m for m in models if m.f_string=='one_1_1'][0]
        self.assertEqual(model.two_1_1.f_string, 'two_1_1')
        
        # one_x_1
        item_one_x_1 = ItemGeneralOne(f_string='one_x_1',
                                      f_integer='1901')
        item_two_1_x = ItemGeneralTwo(f_string='two_1_x',
                                      one_x_1=item_one_x_1)
        persister.persist(item_two_1_x)
        models = self.get_all_models(self.ModelGeneralTwo)
        model = [m for m in models if m.f_string=='two_1_x'][0]
        self.assertEqual(model.one_x_1.f_string, 'one_x_1') 
        models = self.get_all_models(self.ModelGeneralOne)
        model = [m for m in models if m.f_string=='one_x_1'][0]
        two_1_x = adapter_cls.get_related_x_to_many(model, 'two_1_x')
        self.assertEqual(len(two_1_x), 1)
        self.assertEqual(two_1_x[0].f_string, 'two_1_x')
        
        
    def test_forward_and_reverse_relations_persist(self):
        class ItemGeneralOne(Item):
            model_cls = self.ModelGeneralOne
        
        class ItemGeneralTwo(Item):
            model_cls = self.ModelGeneralTwo
        
        adapter_cls = get_adapter_cls(self.ModelGeneralOne)
        persister = self.persister
        
        #--- from item_one ---
        item_one = ItemGeneralOne()
        item_one['two_1_1'] = ItemGeneralTwo(f_integer='101')
        item_one['two_x_1'] = ItemGeneralTwo(f_integer='901')
        item_one['two_x_x'].gen(f_integer='909')
        
        persister.persist(item_one)
        models = self.get_all_models(self.ModelGeneralOne)
        
        self.assertEqual(len(models), 1)
        model = models[0]
        self.assertEqual(model.two_1_1.f_integer, 101)
        self.assertEqual(model.two_x_1.f_integer, 901)
        two_x_x = adapter_cls.get_related_x_to_many(model, 'two_x_x')
        self.assertEqual(len(two_x_x), 1)
        self.assertEqual(two_x_x[0].f_integer, 909)
        
        #--- from item two ---
        item_two = ItemGeneralTwo(f_string='second item')
        item_two['one_1_1'] = ItemGeneralOne(f_integer='2101')
        item_two['one_x_1'] = ItemGeneralOne(f_integer='2901')
        item_two['one_x_x'].gen(f_integer='2909')
        
        persister.persist(item_two)
        models = self.get_all_models(self.ModelGeneralTwo)
        
        #self.assertEqual(len(models), 4)  # 3 before and 1 now
        model = [m for m in models if m.f_string=='second item'][0]
        self.assertEqual(model.one_1_1.f_integer, 2101)
        self.assertEqual(model.one_x_1.f_integer, 2901)
        one_x_x = adapter_cls.get_related_x_to_many(model, 'one_x_x')
        self.assertEqual(len(one_x_x), 1)
        self.assertEqual(one_x_x[0].f_integer, 2909)
        
        #--- from self to self ---
        item_one = ItemGeneralOne(f_string='third item')
        # parent
        item_one['parent_1_1'] = ItemGeneralOne(f_integer='3101')
        item_one['parent_x_1'] = ItemGeneralOne(f_integer='3901')
        item_one['parent_x_x'].gen(f_integer='3909')
        # child
        item_one['child_1_1'] = ItemGeneralOne(f_integer='4101')
        item_one['child_1_x'].gen(f_integer='4109')
        item_one['child_x_x'].gen(f_integer='4909')
        
        persister.persist(item_one)
        models = self.get_all_models(self.ModelGeneralOne)
        model = [m for m in models if m.f_string=='third item'][0]
        
        # parent
        self.assertEqual(model.parent_1_1.f_integer, 3101)
        self.assertEqual(model.parent_x_1.f_integer, 3901)
        parent_x_x = adapter_cls.get_related_x_to_many(model, 'parent_x_x')
        self.assertEqual(len(parent_x_x), 1)
        self.assertEqual(parent_x_x[0].f_integer, 3909)
        
        # child
        self.assertEqual(model.child_1_1.f_integer, 4101)
        child_1_x = adapter_cls.get_related_x_to_many(model, 'child_1_x')
        self.assertEqual(len(child_1_x), 1)
        self.assertEqual(child_1_x[0].f_integer, 4109)
        child_x_x = adapter_cls.get_related_x_to_many(model, 'child_x_x')
        self.assertEqual(len(child_x_x), 1)
        self.assertEqual(child_x_x[0].f_integer, 4909)
        

    def text_one_to_many_getter(self):
        class ItemGeneralOne(Item):
            model_cls = self.ModelGeneralOne
            creators = ['f_integer']
            getters = ['f_integer', 'two_1_x']
        
        class ItemGeneralTwo(Item):
            model_cls = self.ModelGeneralTwo
            creators = ['f_integer']
            getters = ['f_integer']
        
        adapter_cls = get_adapter_cls(self.ModelGeneralOne)
        persister = self.persister
        
        # creating dummy records
        bulk_item_one = ItemGeneralOne.Bulk()
        bulk_item_two = ItemGeneralTwo.Bulk()
        for f_integer in range(1, 4):  # 1..3
            bulk_item_one.gen(f_integer=1000+f_integer)
            bulk_item_two.gen(f_integer=1000+f_integer)
        
        persister.persist(bulk_item_one)
        persister.persist(bulk_item_two)
        
        #--- one-to-many -------------------------------------------------------
        
        # creating item one
        item_one = ItemGeneralOne(f_integer=2001)  # new
        item_one['two_1_x'].gen(f_integer=1003)  # old
        item_one['two_1_x'].gen(f_integer=1004)  # new
        
        _, model_lists = persister.persist(item_one)
        
        self.assertEqual(len(self.get_all_models(self.ModelGeneralOne)), 4)
        self.assertEqual(len(self.get_all_models(self.ModelGeneralTwo)), 4)
        self.assertEqual(len(model_lists), 1)
        self.assertEqual(len(model_lists[0]), 1)
        
        model = model_lists[0][0]
        two_1_x = adapter_cls.get_related_x_to_many(model, 'two_1_x')
        self.assertEqual(len(two_1_x), 2)
        two_1_x.sort(key=lambda m: m.f_integer)
        self.assertEqual(two_1_x[0].f_integer, 1003)
        self.assertEqual(two_1_x[1].f_integer, 1004)
        
        # updating item one
        item_one = ItemGeneralOne()  # old, will be found by "two_1_x"
        item_one['two_1_x'].gen(f_integer=1004)  # old
        item_one['two_1_x'].gen(f_integer=1005)  # new
        
        _, model_lists = persister.persist(item_one)
        self.assertEqual(len(self.get_all_models(self.ModelGeneralOne)), 4)
        self.assertEqual(len(self.get_all_models(self.ModelGeneralTwo)), 5)
        self.assertEqual(len(model_lists), 1)
        self.assertEqual(len(model_lists[0]), 1)
        
        model = model_lists[0][0]
        self.assertEqual(model.f_integer, 2001)
        two_1_x = adapter_cls.get_related_x_to_many(model, 'two_1_x')
        self.assertEqual(len(two_1_x), 3)
        two_1_x.sort(key=lambda m: m.f_integer)
        self.assertEqual(two_1_x[0].f_integer, 1003)
        self.assertEqual(two_1_x[1].f_integer, 1004)
        self.assertEqual(two_1_x[2].f_integer, 1005)
        
        # empty bulk must be ignored
        item_one = ItemGeneralOne()
        item_one['two_1_x']  # accessing the bulk creates it
        items, model_lists = persister.persist(item_one)
        self.assertEqual(len(items), 0)
        self.assertEqual(len(model_lists), 0)
        # nothing changed
        self.assertEqual(len(self.get_all_models(self.ModelGeneralOne)), 4)
        self.assertEqual(len(self.get_all_models(self.ModelGeneralTwo)), 5)

    
    def text_many_to_many_getter(self):
        class ItemGeneralOne(Item):
            model_cls = self.ModelGeneralOne
            creators = ['f_integer']
            getters = ['f_integer']
        
        class ItemGeneralTwo(Item):
            model_cls = self.ModelGeneralTwo
            creators = ['f_integer']
            getters = ['f_integer', 'one_x_x']
        
        adapter_cls = get_adapter_cls(self.ModelGeneralOne)
        persister = self.persister
        
        # creating dummy records
        bulk_item_one = ItemGeneralOne.Bulk()
        bulk_item_two = ItemGeneralTwo.Bulk()
        for f_integer in range(1, 4):  # 1..3
            bulk_item_one.gen(f_integer=1000+f_integer)
            bulk_item_two.gen(f_integer=1000+f_integer)
        
        persister.persist(bulk_item_one)
        persister.persist(bulk_item_two)
        
        #--- many-to-many ------------------------------------------------------
        
        # creating item two
        item_two = ItemGeneralTwo(f_integer=2001)  # new
        item_two['one_x_x'].gen(f_integer=1003)  # old
        item_two['one_x_x'].gen(f_integer=1004)  # new
        
        _, model_lists = persister.persist(item_two)
        
        self.assertEqual(len(self.get_all_models(self.ModelGeneralOne)), 4)
        self.assertEqual(len(self.get_all_models(self.ModelGeneralTwo)), 4)
        self.assertEqual(len(model_lists), 1)
        self.assertEqual(len(model_lists[0]), 1)
        
        model = model_lists[0][0]
        one_x_x = adapter_cls.get_related_x_to_many(model, 'one_x_x')
        self.assertEqual(len(one_x_x), 2)
        one_x_x.sort(key=lambda m: m.f_integer)
        self.assertEqual(one_x_x[0].f_integer, 1003)
        self.assertEqual(one_x_x[1].f_integer, 1004)
        
        # updating item one
        item_two = ItemGeneralTwo()  # old, will be found by "one_x_x"
        item_two['one_x_x'].gen(f_integer=1004)  # old
        item_two['one_x_x'].gen(f_integer=1005)  # new
        
        _, model_lists = persister.persist(item_two)
        self.assertEqual(len(self.get_all_models(self.ModelGeneralOne)), 5)
        self.assertEqual(len(self.get_all_models(self.ModelGeneralTwo)), 4)
        self.assertEqual(len(model_lists), 1)
        self.assertEqual(len(model_lists[0]), 1)
        
        model = model_lists[0][0]
        self.assertEqual(model.f_integer, 2001)
        one_x_x = adapter_cls.get_related_x_to_many(model, 'one_x_x')
        self.assertEqual(len(one_x_x), 3)
        one_x_x.sort(key=lambda m: m.f_integer)
        self.assertEqual(one_x_x[0].f_integer, 1003)
        self.assertEqual(one_x_x[1].f_integer, 1004)
        self.assertEqual(one_x_x[2].f_integer, 1005)
        
        # empty bulk must be ignored
        item_two = ItemGeneralTwo()
        item_two['one_x_x']  # accessing the bulk creates it
        items, model_lists = persister.persist(item_two)
        self.assertEqual(len(items), 0)
        self.assertEqual(len(model_lists), 0)
        # nothing changed
        self.assertEqual(len(self.get_all_models(self.ModelGeneralOne)), 5)
        self.assertEqual(len(self.get_all_models(self.ModelGeneralTwo)), 4)
    
    
    def text_one_to_many_getter_mix(self):
        class ItemGeneralOne(Item):
            model_cls = self.ModelGeneralOne
            creators = ['f_integer']
            getters = ['f_integer']
        
        class ItemGeneralTwo(Item):
            model_cls = self.ModelGeneralTwo
            creators = ['f_integer']
            getters = ['f_integer', {'f_float', 'one_1_x'}]
        
        adapter_cls = get_adapter_cls(self.ModelGeneralOne)
        persister = self.persister
        
        # creating dummy records
        bulk_item_one = ItemGeneralOne.Bulk()
        bulk_item_two = ItemGeneralTwo.Bulk()
        for f_integer in range(1, 4):  # 1..3
            bulk_item_one.gen(f_integer=1000+f_integer,
                              f_float=1000.1+f_integer)
            bulk_item_two.gen(f_integer=1000+f_integer,
                              f_float=1000.1+f_integer)
        
        persister.persist(bulk_item_one)
        persister.persist(bulk_item_two)
        
        #--- mix with regular filter -------------------------------------------
        
        # creating item_two
        item_two = ItemGeneralTwo(f_integer=2001, f_float=2001.2)  # new
        item_two['one_1_x'].gen(f_integer=1003)  # old
        item_two['one_1_x'].gen(f_integer=1004)  # new
        
        _, model_lists = persister.persist(item_two)
        
        self.assertEqual(len(self.get_all_models(self.ModelGeneralOne)), 4)
        self.assertEqual(len(self.get_all_models(self.ModelGeneralTwo)), 4)
        self.assertEqual(len(model_lists), 1)
        self.assertEqual(len(model_lists[0]), 1)
        
        model = model_lists[0][0]
        one_1_x = adapter_cls.get_related_x_to_many(model, 'one_1_x')
        self.assertEqual(len(one_1_x), 2)
        one_1_x.sort(key=lambda m: m.f_integer)
        self.assertEqual(one_1_x[0].f_integer, 1003)
        self.assertEqual(one_1_x[1].f_integer, 1004)
        
        # updating item
        # (can find by `f_float`, but item from `one_1_x` is not there)
        item_two = ItemGeneralTwo(f_float=2001.2)
        item_two['one_1_x'].gen(f_integer=1001)  # old
        
        _, model_lists = persister.persist(item_two)
        self.assertEqual(len(self.get_all_models(self.ModelGeneralOne)), 4)
        self.assertEqual(len(self.get_all_models(self.ModelGeneralTwo)), 4)
        self.assertEqual(len(model_lists), 0)
        
        # (can find by `one_1_x`, but `f_float` does not match)
        item_two = ItemGeneralTwo(f_float=2002.2)
        item_two['one_1_x'].gen(f_integer=1004)  # old
        
        _, model_lists = persister.persist(item_two)
        self.assertEqual(len(self.get_all_models(self.ModelGeneralOne)), 4)
        self.assertEqual(len(self.get_all_models(self.ModelGeneralTwo)), 4)
        self.assertEqual(len(model_lists), 0)
        
        # (empty bulk)
        item_two = ItemGeneralTwo(f_float=2002.2)
        item_two['one_1_x']  # accessing bulk creates it
        
        _, model_lists = persister.persist(item_two)
        self.assertEqual(len(self.get_all_models(self.ModelGeneralOne)), 4)
        self.assertEqual(len(self.get_all_models(self.ModelGeneralTwo)), 4)
        
        # now update must succeed
        item_two = ItemGeneralTwo(f_float=2001.2)
        item_two['one_1_x'].gen(f_integer=1004)  # old
        item_two['one_1_x'].gen(f_integer=1005)  # new
        
        _, model_lists = persister.persist(item_two)
        self.assertEqual(len(self.get_all_models(self.ModelGeneralOne)), 5)
        self.assertEqual(len(self.get_all_models(self.ModelGeneralTwo)), 4)
        
        self.assertEqual(len(model_lists), 1)
        self.assertEqual(len(model_lists[0]), 1)
        model = model_lists[0][0]
        one_1_x = adapter_cls.get_related_x_to_many(model, 'one_1_x')
        self.assertEqual(len(one_1_x), 3)
        one_1_x.sort(key=lambda m: m.f_integer)
        self.assertEqual(one_1_x[0].f_integer, 1003)
        self.assertEqual(one_1_x[1].f_integer, 1004)
        self.assertEqual(one_1_x[2].f_integer, 1005)
        
    
    def text_many_to_many_getter_mix(self):
        class ItemGeneralOne(Item):
            model_cls = self.ModelGeneralOne
            creators = ['f_integer']
            getters = ['f_integer']
        
        class ItemGeneralTwo(Item):
            model_cls = self.ModelGeneralTwo
            creators = ['f_integer']
            getters = ['f_integer', {'f_float', 'one_x_x'}]
        
        adapter_cls = get_adapter_cls(self.ModelGeneralOne)
        persister = self.persister
        
        # creating dummy records
        bulk_item_one = ItemGeneralOne.Bulk()
        bulk_item_two = ItemGeneralTwo.Bulk()
        for f_integer in range(1, 4):  # 1..3
            bulk_item_one.gen(f_integer=1000+f_integer,
                              f_float=1000.1+f_integer)
            bulk_item_two.gen(f_integer=1000+f_integer,
                              f_float=1000.1+f_integer)
        
        persister.persist(bulk_item_one)
        persister.persist(bulk_item_two)
        
        #--- mix with regular filter -------------------------------------------
        
        # creating item_two
        item_two = ItemGeneralTwo(f_integer=2001, f_float=2001.2)  # new
        item_two['one_x_x'].gen(f_integer=1003)  # old
        item_two['one_x_x'].gen(f_integer=1004)  # new
        
        _, model_lists = persister.persist(item_two)
        
        self.assertEqual(len(self.get_all_models(self.ModelGeneralOne)), 4)
        self.assertEqual(len(self.get_all_models(self.ModelGeneralTwo)), 4)
        self.assertEqual(len(model_lists), 1)
        self.assertEqual(len(model_lists[0]), 1)
        
        model = model_lists[0][0]
        one_x_x = adapter_cls.get_related_x_to_many(model, 'one_x_x')
        self.assertEqual(len(one_x_x), 2)
        one_x_x.sort(key=lambda m: m.f_integer)
        self.assertEqual(one_x_x[0].f_integer, 1003)
        self.assertEqual(one_x_x[1].f_integer, 1004)
        
        # updating item
        # (can find by `f_float`, but item from `one_x_x` is not there)
        item_two = ItemGeneralTwo(f_float=2001.2)
        item_two['one_x_x'].gen(f_integer=1001)  # old
        
        _, model_lists = persister.persist(item_two)
        self.assertEqual(len(self.get_all_models(self.ModelGeneralOne)), 4)
        self.assertEqual(len(self.get_all_models(self.ModelGeneralTwo)), 4)
        self.assertEqual(len(model_lists), 0)
        
        # (can find by `one_x_x`, but `f_float` does not match)
        item_two = ItemGeneralTwo(f_float=2002.2)
        item_two['one_x_x'].gen(f_integer=1004)  # old
        
        _, model_lists = persister.persist(item_two)
        self.assertEqual(len(self.get_all_models(self.ModelGeneralOne)), 4)
        self.assertEqual(len(self.get_all_models(self.ModelGeneralTwo)), 4)
        self.assertEqual(len(model_lists), 0)
        
        # (empty bulk)
        item_two = ItemGeneralTwo(f_float=2002.2)
        item_two['one_x_x']  # accessing bulk creates it
        
        _, model_lists = persister.persist(item_two)
        self.assertEqual(len(self.get_all_models(self.ModelGeneralOne)), 4)
        self.assertEqual(len(self.get_all_models(self.ModelGeneralTwo)), 4)
        
        # now update must succeed
        item_two = ItemGeneralTwo(f_float=2001.2)
        item_two['one_x_x'].gen(f_integer=1004)  # old
        item_two['one_x_x'].gen(f_integer=1005)  # new
        
        _, model_lists = persister.persist(item_two)
        self.assertEqual(len(self.get_all_models(self.ModelGeneralOne)), 5)
        self.assertEqual(len(self.get_all_models(self.ModelGeneralTwo)), 4)
        
        self.assertEqual(len(model_lists), 1)
        self.assertEqual(len(model_lists[0]), 1)
        model = model_lists[0][0]
        one_x_x = adapter_cls.get_related_x_to_many(model, 'one_x_x')
        self.assertEqual(len(one_x_x), 3)
        one_x_x.sort(key=lambda m: m.f_integer)
        self.assertEqual(one_x_x[0].f_integer, 1003)
        self.assertEqual(one_x_x[1].f_integer, 1004)
        self.assertEqual(one_x_x[2].f_integer, 1005)
    
    
    def test_one_to_many_creator(self):
        class ItemGeneralOne(Item):
            model_cls = self.ModelGeneralOne
            creators = ['two_1_x']
        
        class ItemGeneralTwo(Item):
            model_cls = self.ModelGeneralTwo
            creators = ['f_integer']
        
        adapter_cls = get_adapter_cls(self.ModelGeneralOne)
        persister = self.persister
        
        # failed creation    
        item_1 = ItemGeneralOne()
        item_1['two_1_x']  # access creates
        
        items, model_lists = persister.persist(item_1)
        self.assertEqual(len(items), 0)
        self.assertEqual(len(model_lists), 0)
        
        # successful creation
        item_1['two_1_x'].gen(f_integer=10)
        items, model_lists = persister.persist(item_1)
        self.assertEqual(len(items), 1)
        self.assertEqual(len(model_lists), 1)
        self.assertEqual(len(model_lists[0]), 1)
        self.assertEqual(len(self.get_all_models(self.ModelGeneralOne)), 1)
        self.assertEqual(len(self.get_all_models(self.ModelGeneralTwo)), 1)
        
        model = model_lists[0][0]
        two_1_x = adapter_cls.get_related_x_to_many(model, 'two_1_x')
        self.assertEqual(len(two_1_x), 1)
        self.assertEqual(two_1_x[0].f_integer, 10)
    
    
    def test_many_to_many_creator(self):
        class ItemGeneralOne(Item):
            model_cls = self.ModelGeneralOne
            creators = ['two_x_x']
        
        class ItemGeneralTwo(Item):
            model_cls = self.ModelGeneralTwo
            creators = ['f_integer']
        
        adapter_cls = get_adapter_cls(self.ModelGeneralOne)
        persister = self.persister
        
        # failed creation    
        item_1 = ItemGeneralOne()
        item_1['two_x_x']  # access creates
        
        items, model_lists = persister.persist(item_1)
        self.assertEqual(len(items), 0)
        self.assertEqual(len(model_lists), 0)
        
        # successful creation
        item_1['two_x_x'].gen(f_integer=10)
        items, model_lists = persister.persist(item_1)
        self.assertEqual(len(items), 1)
        self.assertEqual(len(model_lists), 1)
        self.assertEqual(len(model_lists[0]), 1)
        self.assertEqual(len(self.get_all_models(self.ModelGeneralOne)), 1)
        self.assertEqual(len(self.get_all_models(self.ModelGeneralTwo)), 1)
        
        model = model_lists[0][0]
        two_x_x = adapter_cls.get_related_x_to_many(model, 'two_x_x')
        self.assertEqual(len(two_x_x), 1)
        self.assertEqual(two_x_x[0].f_integer, 10)
    
    
    def test_x_to_many_getters(self):
        class ItemGeneralOne(Item):
            model_cls = self.ModelGeneralOne
            creators = ['f_integer']
            getters = ['f_string']
        
        class ItemGeneralTwo(Item):
            model_cls = self.ModelGeneralTwo
            creators = ['f_integer']
            getters = ['one_x_x']
        
        adapter_cls = get_adapter_cls(self.ModelGeneralOne)
        persister = self.persister
        
        item_one = ItemGeneralOne(f_integer='1', f_string='str-1')
        item_two = ItemGeneralTwo(f_integer='2', one_x_x=[item_one])

        persister.persist(item_two)
        self.assertEqual(len(self.get_all_models(self.ModelGeneralOne)), 1)
        self.assertEqual(len(self.get_all_models(self.ModelGeneralTwo)), 1)
        
        item_one = ItemGeneralOne(f_string='str-1')
        item_two = ItemGeneralTwo(f_string='str-2', one_x_x=[item_one])
        
        persister.persist(item_two)
        self.assertEqual(len(self.get_all_models(self.ModelGeneralOne)), 1)
        self.assertEqual(len(self.get_all_models(self.ModelGeneralTwo)), 1)
        
        model_one = self.get_all_models(self.ModelGeneralOne)[0]
        model_two = self.get_all_models(self.ModelGeneralTwo)[0]
        
        self.assertEqual(model_one.f_integer, 1)
        self.assertEqual(model_one.f_string, 'str-1')
        related_two = adapter_cls.get_related_x_to_many(model_one, 'two_x_x')
        self.assertEqual(len(related_two), 1)
        self.assertEqual(model_two, related_two[0])
        
        self.assertEqual(model_two.f_integer, 2)
        self.assertEqual(model_two.f_string, 'str-2')
        related_one = adapter_cls.get_related_x_to_many(model_two, 'one_x_x')
        self.assertEqual(len(related_one), 1)
        self.assertEqual(model_one, related_one[0])
        
        
    def test_multiple_same_models_returned(self):
        class ItemGeneralOne(Item):
            model_cls = self.ModelGeneralOne
            creators = ['f_integer']
            getters = ['two_x_x', 'f_string']
        
        class ItemGeneralTwo(Item):
            model_cls = self.ModelGeneralTwo
            creators = ['f_integer']
            getters = ['f_string']
        
        adapter_cls = get_adapter_cls(self.ModelGeneralOne)
        persister = self.persister
        
        item_one = ItemGeneralOne(f_integer='1', f_string='str-1')
        item_two_1 = ItemGeneralTwo(f_integer='2', f_string='str-2')
        item_two_2 = ItemGeneralTwo(f_integer='3', f_string='str-3')
        # through x-to-many relation same model can be loaded twice
        item_one['two_x_x'].add(item_two_1, item_two_2)
        
        def ensure_saved_models():
            models_one = self.get_all_models(self.ModelGeneralOne)
            models_two = self.get_all_models(self.ModelGeneralTwo,
                                             sort_key=lambda x: x.f_integer)
            self.assertEqual(len(models_one), 1)
            self.assertEqual(len(models_two), 2)
            model_one = self.get_all_models(self.ModelGeneralOne)[0]
            model_two_1 = self.get_all_models(self.ModelGeneralTwo)[0]
            model_two_2 = self.get_all_models(self.ModelGeneralTwo)[1]
            
            self.assertEqual(model_one.f_integer, 1)
            self.assertEqual(model_one.f_string, 'str-1')
            related_two = adapter_cls.get_related_x_to_many(model_one, 'two_x_x')
            related_two.sort(key=lambda x: x.f_integer)
            self.assertEqual(len(related_two), 2)
            self.assertEqual(model_two_1, related_two[0])
            self.assertEqual(model_two_2, related_two[1])
            
            self.assertEqual(model_two_1.f_integer, 2)
            self.assertEqual(model_two_1.f_string, 'str-2')
            related_one = adapter_cls.get_related_x_to_many(model_two_1,
                                                            'one_x_x')
            self.assertEqual(len(related_one), 1)
            self.assertEqual(model_one, related_one[0])
            
            self.assertEqual(model_two_2.f_integer, 3)
            self.assertEqual(model_two_2.f_string, 'str-3')
            related_one = adapter_cls.get_related_x_to_many(model_two_2,
                                                            'one_x_x')
            self.assertEqual(len(related_one), 1)
            self.assertEqual(model_one, related_one[0])
        
        persister.persist(item_one)
        ensure_saved_models()
        
        # saving models second time might cause same model to be returned
        # for ['two_x_x', 'f_string'] getters
        persister.persist(item_one)
        ensure_saved_models()
    
    def test_persist_no_reverse_relations(self):
        class ItemAutoReverseOne(Item):
            model_cls = self.ModelAutoReverseOne
        
        class ItemAutoReverseTwoA(Item):
            model_cls = self.ModelAutoReverseTwoA
        
        class ItemAutoReverseTwoB(Item):
            model_cls = self.ModelAutoReverseTwoB
        
        class ItemAutoReverseThreeA(Item):
            model_cls = self.ModelAutoReverseThreeA
        
        class ItemAutoReverseThreeB(Item):
            model_cls = self.ModelAutoReverseThreeB
        
        class ItemAutoReverseFourA(Item):
            model_cls = self.ModelAutoReverseFourA
        
        class ItemAutoReverseFourB(Item):
            model_cls = self.ModelAutoReverseFourB

        
        item = ItemAutoReverseOne(f_string='one')
        
        item['two_b_1_1'] = ItemAutoReverseTwoB(f_string='two_b_1_1')
        item['three_b_x_1'] = ItemAutoReverseThreeB(f_string='three_b_x_1')
        item['four_b_x_x'].gen(f_string='four_b_x_x_first')
        item['four_b_x_x'].gen(f_string='four_b_x_x_second')
        
        persister = self.persister
        _, models_one_list = persister.persist(item)
        self.assertTrue(len(models_one_list), 1)
        models_one = models_one_list[0]
        self.assertTrue(len(models_one), 1)
        model_one_returned = models_one[0]
        
        # one
        models_one = self.get_all_models(self.ModelAutoReverseOne)
        self.assertEqual(len(models_one), 1)
        model_one = models_one[0]
        
        self.assertEqual(model_one, model_one_returned)
        
        # two
        models_two = self.get_all_models(self.ModelAutoReverseTwoB)
        self.assertEqual(len(models_two), 1)
        model_two = models_two[0]
        
        self.assertEqual(model_one.two_b_1_1, model_two)
        
        # three
        models_three = self.get_all_models(self.ModelAutoReverseThreeB)
        self.assertEqual(len(models_three), 1)
        model_three = models_three[0]
        
        self.assertEqual(model_one.three_b_x_1, model_three)
        
        # four
        sort_func = lambda model: model.f_string
        
        models_four = self.get_all_models(self.ModelAutoReverseFourB,
                                          sort_key=sort_func)
        self.assertEqual(len(models_four), 2)
        
        related_models_four = self.get_related_x_to_many(model_one,
                                                         'four_b_x_x',
                                                         sort_key=sort_func)
        self.assertEqual(len(related_models_four), 2)
        for model_four, related_model_for in zip(models_four,
                                                 related_models_four):
            self.assertEqual(model_four, related_model_for)
    
    
    def test_related_x_to_many_contains(self):
        class ItemGeneralOne(Item):
            model_cls = self.ModelGeneralOne
            creators = ['f_integer']
            getters = ['f_integer']
        
        class ItemGeneralTwo(Item):
            model_cls = self.ModelGeneralTwo
            creators = ['f_integer']
            getters = ['f_integer']
        
        persister = self.persister
        adapter_cls = persister.adapter_cls
        
        for f_key in ['two_1_x', 'two_x_x']:
            item_one_1 = ItemGeneralOne(f_integer='1000')
            item_one_1[f_key].gen(f_integer='1001')
            item_one_1[f_key].gen(f_integer='1002')
            
            item_one_2 = ItemGeneralOne(f_integer='2000')
            item_one_2[f_key].gen(f_integer='2001')
            item_one_2[f_key].gen(f_integer='2002')
            
            persister.persist(item_one_1)
            persister.persist(item_one_2)
            
            sort_func = lambda model: model.f_integer
            
            model_ones = self.get_all_models(self.ModelGeneralOne,
                                             sort_key=sort_func)
            self.assertEqual(len(model_ones), 2)
            model_one_1000, model_one_2000 = model_ones
            
            models_two_1 = adapter_cls.get_related_x_to_many(model_one_1000,
                                                             f_key)
            self.assertEqual(len(models_two_1), 2)
            model_two_1001, model_two_1002 = models_two_1
            
            models_two_2 = adapter_cls.get_related_x_to_many(model_one_2000,
                                                             f_key)
            self.assertEqual(len(models_two_2), 2)
            model_two_2001, model_two_2002 = models_two_2
            
            self.assertEqual(model_one_1000.f_integer, 1000)
            self.assertEqual(model_one_2000.f_integer, 2000)
            self.assertEqual(model_two_1001.f_integer, 1001)
            self.assertEqual(model_two_1002.f_integer, 1002)
            self.assertEqual(model_two_2001.f_integer, 2001)
            self.assertEqual(model_two_2002.f_integer, 2002)
            
            # the testing
            models_two = adapter_cls.related_x_to_many_contains(
                model_one_1000, f_key, [model_two_1001, model_two_1002,
                                        model_two_2001, model_two_2002],
                persister.adapter_settings)
            self.assertEqual(len(models_two), 2)
            models_two.sort(key=sort_func)
            self.assertEqual(models_two[0].f_integer, 1001)
            self.assertEqual(models_two[1].f_integer, 1002)
            # exectly the same models returned
            self.assertIs(model_two_1001, models_two[0])
            self.assertIs(model_two_1002, models_two[1])
            
            models_two = adapter_cls.related_x_to_many_contains(
                model_one_1000, f_key, [model_two_1001, model_two_2002],
                persister.adapter_settings)
            self.assertEqual(len(models_two), 1)
            self.assertEqual(models_two[0].f_integer, 1001)
            self.assertIs(model_two_1001, models_two[0])
            
            models_two = adapter_cls.related_x_to_many_contains(
                model_one_1000, f_key, [model_two_2001, model_two_2002],
                persister.adapter_settings)
            self.assertEqual(len(models_two), 0)
            
            models_two = adapter_cls.related_x_to_many_contains(
                model_one_1000, f_key, [], persister.adapter_settings)
            self.assertEqual(len(models_two), 0)

        
    def test_merging_items_in_bulks(self):
        class ItemGeneralOne(Item):
            model_cls = self.ModelGeneralOne
            creators = ['f_integer']
            getters = ['f_integer']
            allow_merge_items = True
        
        class ItemGeneralTwo(Item):
            model_cls = self.ModelGeneralTwo
            creators = ['f_integer']
            getters = ['f_integer']
            allow_merge_items = True
        
        # one
        item_one_1 = ItemGeneralOne(f_integer='1000')
        
        # two
        item_one_1['two_1_x'].gen(f_integer='1001',
                                  f_text='text-1')
        item_two_2 = item_one_1['two_1_x'].gen(f_integer='1001',
                                               f_string='str-1')
        
        # one
        item_two_2['one_x_x'].gen(f_integer='2001',
                                  f_text='text-2')
        item_two_2['one_x_x'].gen(f_integer='2001',
                                  f_string='str-2')
        # not mergable
        item_two_2['one_x_x'].gen(f_integer='9999',
                                  f_string='str-9')
        item_one_1.process()
        
        expect = {
            'id': 1,
            'item': {
                'f_integer': 1000,
                'two_1_x': {
                    'bulk': [
                        {
                            'id': 2,
                            'item': {
                                'f_integer': 1001,
                                'f_string': 'str-1',
                                'f_text': 'text-1',
                                'one_x_1': {
                                    'id': 1
                                },
                                'one_x_x': {
                                    'bulk': [
                                        {
                                            'item': {
                                                'f_integer': 2001,
                                                'f_string': 'str-2',
                                                'f_text': 'text-2',
                                                'two_x_x': {
                                                    'bulk': [
                                                        {
                                                            'id': 2
                                                        }
                                                    ],
                                                    'defaults': {}
                                                }
                                            }
                                        },
                                        {
                                            'item': {
                                                'f_integer': 9999,
                                                'f_string': 'str-9',
                                                'two_x_x': {
                                                    'bulk': [
                                                        {
                                                            'id': 2
                                                        }
                                                    ],
                                                    'defaults': {}
                                                }
                                            }
                                        }
                                    ],
                                    'defaults': {}
                                }
                            }
                        }
                    ],
                    'defaults': {}
                }
            }
        }
        self.assertEqual(item_one_1.to_dict(), expect)
        
        # merging at top level
        bulk_one = ItemGeneralOne.Bulk()
        bulk_one.gen(f_integer='1', f_string='str-1')
        bulk_one.gen(f_integer='1', f_text='text-1')
        bulk_one.process()
        
        expect = {
            'bulk': [
                {
                    'item': {
                        'f_integer': 1,
                        'f_string': 'str-1',
                        'f_text': 'text-1'
                    }
                }
            ],
            'defaults': {}
        }
        self.assertEqual(bulk_one.to_dict(), expect)
        
    def test_no_item_returned_with_fkey(self):
        class ItemGeneralOne(Item):
            model_cls = self.ModelGeneralOne
            creators = [['f_integer', 'two_1_1']]
            getters = [['f_integer', 'two_1_1']]
        
        class ItemGeneralTwo(Item):
            model_cls = self.ModelGeneralTwo
            creators = ['f_integer']
            getters = ['f_integer']
            
        persister = self.persister
        adapter_cls = persister.adapter_cls
        
        item_one = ItemGeneralOne(f_integer=1)
        item_one['two_1_1'](f_integer=2)
        
        persister.persist(item_one)
        models_one = self.get_all_models(self.ModelGeneralOne)
        self.assertEqual(len(models_one), 1)
        model_one = models_one[0]
        self.assertEqual(model_one.f_integer, 1)
        self.assertIsNotNone(model_one.two_1_1)
        self.assertEqual(model_one.two_1_1.f_integer, 2)
        
        item_one = ItemGeneralOne(f_integer=1)
        item_one['two_1_1'](f_integer=2)
        items_and_fkeys = [[item_one, {}],]
        got_models = adapter_cls.get(items_and_fkeys,
                                     persister.adapter_settings)
        self.assertFalse(bool(got_models),
                         'Adapter returned models that have relations in '
                         'getter when empty `fkey`. Probably adapter '
                         'just returned all models from DB.')
    
    
    def test_batch_size(self):
        class ItemGeneralOne(Item):
            model_cls = self.ModelGeneralOne
            creators = [{'f_integer'}]
            getters = [{'f_integer'}]
        
        # need this for `ItemGeneralOne` (related field)
        class ItemGeneralTwo(Item):
            model_cls = self.ModelGeneralTwo
        
        persister = self.persister
        adapter_cls = persister.adapter_cls
        original_adapter_batch_size = adapter_cls.BATCH_SIZE
        original_adapter_get = adapter_cls.get
        list_of_get_sizes = []
        def decorated_adapter_get(items_and_fkeys, *args, **kwargs):
            nonlocal list_of_get_sizes
            list_of_get_sizes.append(len(items_and_fkeys))
            return original_adapter_get(items_and_fkeys, *args, **kwargs)
        adapter_cls.get = decorated_adapter_get
        
        try:
            # unlimited batch size
            adapter_cls.BATCH_SIZE = 1000
            bulk = ItemGeneralOne.Bulk()
            for i in range(10):
                bulk.gen(f_integer=i)
            persister.persist(bulk)
            # got everything in one batch
            self.assertEqual(list_of_get_sizes, [10])
            list_of_get_sizes.clear()
            
            adapter_cls.BATCH_SIZE = 3
            persister.persist(bulk)
            # 4 batches with max size of 3
            self.assertEqual(list_of_get_sizes, [3, 3, 3, 1])
            list_of_get_sizes.clear()
            
            # unlimited again
            adapter_cls.BATCH_SIZE = 1000
            persister.persist(bulk)
            self.assertEqual(list_of_get_sizes, [10])
            list_of_get_sizes.clear()
            
            # limit on item class side
            ItemGeneralOne.batch_size = 4
            persister.persist(bulk)
            # 2 batches with max size of 4
            self.assertEqual(list_of_get_sizes, [4, 4, 2])
            list_of_get_sizes.clear()
            
            bulk = ItemGeneralTwo.Bulk()
            for i in range(10):
                bulk.gen(f_integer=i)
            persister.persist(bulk)
            # second class not effected
            self.assertEqual(list_of_get_sizes, [10])
            list_of_get_sizes.clear()
        finally:
            adapter_cls.get = original_adapter_get
            adapter_cls.BATCH_SIZE = original_adapter_batch_size
        
    
    def test_persist_with_scope(self):
        class ItemGeneralOne(Item):
            model_cls = self.ModelGeneralOne
            creators = [{'f_integer'}]
            getters = [{'f_integer'}]
        
        # need this for `ItemGeneralOne` (related field)
        class ItemGeneralTwo(Item):
            model_cls = self.ModelGeneralTwo
            creators = [{'f_integer'}]
            getters = [{'f_integer'}]
            
        scope = Scope(
            {
                ItemGeneralOne: {
                    'creators': ['f_integer', 'f_float'],
                    'getters': ['f_integer', 'f_float'],
                }
            },
            scope_id='test_persist_with_scope')
        
        self.assertNotIsInstance(scope[ItemGeneralOne], ItemGeneralOne)
        
        persister = self.persister
        
        # not scoped
        item_one = ItemGeneralOne(f_integer='100', f_float='200')
        item_one_dump = persister.dumps(item_one)
        item_one_load = persister.loads(item_one_dump)
        self.assertIsInstance(item_one_load, ItemGeneralOne)
        
        
        item_one_scoped = scope[ItemGeneralOne](f_integer='300', f_float='400')
        item_one_scoped_dump = persister.dumps(item_one_scoped)
        item_one_scoped_load = persister.loads(item_one_scoped_dump)
        self.assertIsInstance(item_one_scoped_load, scope[ItemGeneralOne])


    def test_fast_insert(self):
        class ItemGeneralOne(Item):
            model_cls = self.ModelGeneralOne
            creators = [{'f_integer'}]
            getters = [{'f_integer'}]
        
        class ItemGeneralTwo(Item):
            model_cls = self.ModelGeneralTwo
            creators = ['f_integer']
            getters = ['f_integer']
            fast_insert = True
            
        persister = self.persister
        sort_func = lambda model: (model.f_integer, model.f_string)
        
        #--- no fast_insert ---
        item_one = ItemGeneralOne(f_integer=1, f_string='one')
        persister.persist(item_one)
        
        bulk_one = ItemGeneralOne.Bulk()
        bulk_one.gen(f_integer=1, f_string='one-updated')
        bulk_one.gen(f_integer=2, f_string='two')
        persister.persist(bulk_one)
        
        model_ones = self.get_all_models(self.ModelGeneralOne,
                                         sort_key=sort_func)
        self.assertEqual(len(model_ones), 2)
        self.assertEqual(model_ones[0].f_string, 'one-updated')
        self.assertEqual(model_ones[1].f_string, 'two')
        
        #--- fast_insert ---
        item_two = ItemGeneralTwo(f_integer=1, f_string='one')
        persister.persist(item_two)
        
        bulk_two = ItemGeneralTwo.Bulk()
        bulk_two.gen(f_integer=1, f_string='one-updated')
        bulk_two.gen(f_integer=2, f_string='two')
        # although "f_integer" field is a getter, since we use fast_insert,
        # new model will be create without checking for update
        persister.persist(bulk_two)
        
        model_twos = self.get_all_models(self.ModelGeneralTwo,
                                         sort_key=sort_func)
        self.assertEqual(len(model_twos), 3)
        self.assertEqual(model_twos[0].f_integer, 1)
        self.assertEqual(model_twos[0].f_string, 'one')
        self.assertEqual(model_twos[1].f_integer, 1)
        self.assertEqual(model_twos[1].f_string, 'one-updated')
        self.assertEqual(model_twos[2].f_integer, 2)
        self.assertEqual(model_twos[2].f_string, 'two')
    

    def test_model_deleter(self):
        
        class ItemGeneralOne(Item):
            model_cls = self.ModelGeneralOne
            creators = [{'f_integer', 'f_string'}]
            getters = [{'f_integer', 'f_string'}]
            deleter_selectors = ['f_string']
        
        class ItemGeneralTwo(Item):
            model_cls = self.ModelGeneralTwo
        
        persister = self.persister
        get_key = lambda model: (model.f_string, model.f_integer)
        
        # imitating first collection from different sources
        for source_number in range(1, 4):
            for outer_i in range(1, 3):
                bulk = ItemGeneralOne.Bulk(
                    f_string='source-{}'.format(source_number))
                for inner_i in range(1, 3):
                    bulk.gen(f_integer=outer_i*100 + inner_i)
                persister.persist(bulk)
        
        # will delete nothing
        persister.execute_deleter(ItemGeneralOne)
        model_ones = self.get_all_models(self.ModelGeneralOne,
                                         sort_key=get_key)

        model_keys = [get_key(model) for model in model_ones]
        expected = [
            # source-1 first iteration
            ('source-1', 101),
            ('source-1', 102),
            # source-1 second iteration
            ('source-1', 201),
            ('source-1', 202),
            # source-2 first iteration
            ('source-2', 101),
            ('source-2', 102),
            # source-2 second iteration
            ('source-2', 201),
            ('source-2', 202),
            # source-3 first iteration
            ('source-3', 101),
            ('source-3', 102),
            # source-3 second iteration
            ('source-3', 201),
            ('source-3', 202),
        ]
        self.assertEqual(model_keys, expected)
        
        # imitating first collection from different sources
        for source_number in range(2, 4):
            for outer_i in range(2, 3):
                bulk = ItemGeneralOne.Bulk(
                    f_string='source-{}'.format(source_number))
                for inner_i in range(1, 4):
                    bulk.gen(f_integer=outer_i*100 + inner_i)
                persister.persist(bulk)
        
        persister.execute_deleter(ItemGeneralOne)
        model_ones = self.get_all_models(self.ModelGeneralOne,
                                         sort_key=get_key)

        model_keys = [get_key(model) for model in model_ones]
        expected = [
            # source-1 must have been ignored (and not deleted)
            ('source-1', 101),
            ('source-1', 102),
            ('source-1', 201),
            ('source-1', 202),
            # source-2 starts from second iteration
            ('source-2', 201),
            ('source-2', 202),
            ('source-2', 203),  # new model
            # source-3 starts from second iteration
            ('source-3', 201),
            ('source-3', 202),
            ('source-3', 203),  # new model
        ]
        self.assertEqual(model_keys, expected)
        
        
    def test_model_deleter_execute_scoped(self):
        class ItemGeneralOne(Item):
            model_cls = self.ModelGeneralOne
            creators = [{'f_integer', 'f_string'}]
            getters = [{'f_integer', 'f_string'}]
            deleter_selectors = ['f_string']
        
        class ItemGeneralTwo(Item):
            model_cls = self.ModelGeneralTwo
        
        persister = self.persister
        get_key = lambda model: (model.f_string, model.f_integer)
        
        
        test_scope = Scope({},
                           scope_id='test_model_deleter_execute_scoped_dummy')
        persister.persist(test_scope[ItemGeneralOne](
            f_string='source-9000', f_integer='9000'
        ))
        
        
        # imitating first collection from different sources
        for source_number in range(1, 3):
            bulk = ItemGeneralOne.Bulk(
                f_string='source-{}'.format(source_number))
            for inner_i in range(1, 3):
                bulk.gen(f_integer=100 + inner_i)
            persister.persist(bulk)
            
        # will delete nothing
        persister.execute_scope_deleter(ItemGeneralOne.get_scope_id())
        model_ones = self.get_all_models(self.ModelGeneralOne,
                                         sort_key=get_key)

        model_keys = [get_key(model) for model in model_ones]
        expected = [
            # source-1
            ('source-1', 101),
            ('source-1', 102),
            # source-2
            ('source-2', 101),
            ('source-2', 102),
            # from test scope
            ('source-9000', 9000),
        ]
        self.assertEqual(model_keys, expected)
        
        
        # delete without scope
        scope = Scope({}, scope_id='test_model_deleter_execute_scoped')
        ScopedItemGeneralOne = scope[ItemGeneralOne]
        
        for source_number in range(1, 3):
            bulk = ItemGeneralOne.Bulk(
                f_string='source-{}'.format(source_number))
            for inner_i in range(2, 4):
                bulk.gen(f_integer=100 + inner_i)
            persister.persist(bulk)
        
        persister.execute_scope_deleter(ItemGeneralOne.get_scope_id())
        model_ones = self.get_all_models(self.ModelGeneralOne,
                                         sort_key=get_key)

        model_keys = [get_key(model) for model in model_ones]
        expected = [
            # source-1
            ('source-1', 102),
            ('source-1', 103),
            # source-2
            ('source-2', 102),
            ('source-2', 103),
            # from test scope
            ('source-9000', 9000),
        ]
        self.assertEqual(model_keys, expected)
        
        # delete with scope        
        persisted_models = []
        for source_number in range(1, 3):
            bulk = ScopedItemGeneralOne.Bulk(
                f_string='source-{}'.format(source_number))
            for inner_i in range(3, 5):
                bulk.gen(f_integer=100 + inner_i)
            _, models_list = persister.persist(bulk)
            for model_list in models_list:
                persisted_models.extend(model_list)
        
        # before executing making sure that different model deleter was used
        self.assertFalse(ItemGeneralOne.metadata['model_deleter'].selectors)
        self.assertFalse(ItemGeneralOne.metadata['model_deleter'].keepers)
        
        expect_selectors = [
            {'f_string': 'source-1'},
            {'f_string': 'source-2'},
        ]
        scoped_deleter = ScopedItemGeneralOne.metadata['model_deleter']
        self.assertEqual(scoped_deleter.selectors, expect_selectors)
        
        persisted_models.sort(key=lambda model: model.id)
        scoped_deleter.keepers.sort(key=lambda keeper: keeper['id'])
        expect_keepers = [{'id': model.id} for model in persisted_models]
        self.assertTrue(len(expect_keepers) != 0)
        self.assertEqual(scoped_deleter.keepers, expect_keepers)
        
        # creating model without scope
        persister.persist(ItemGeneralOne(f_string='source-9009',
                                         f_integer='9009'))
        
        persister.execute_scope_deleter(ScopedItemGeneralOne.get_scope_id())
        model_ones = self.get_all_models(self.ModelGeneralOne,
                                         sort_key=get_key)

        model_keys = [get_key(model) for model in model_ones]
        expected = [
            # source-1
            ('source-1', 103),
            ('source-1', 104),
            # source-2
            ('source-2', 103),
            ('source-2', 104),
            # from test scope
            ('source-9000', 9000),
            # from not scoped item class with deleter not executed
            ('source-9009', 9009),
        ]
        self.assertEqual(model_keys, expected)
        
        
    def test_model_deleter_execute_on_persist(self):
        class ItemGeneralOne(Item):
            model_cls = self.ModelGeneralOne
            creators = [{'f_integer', 'f_string'}]
            getters = [{'f_integer', 'f_string'}]
            deleter_selectors = ['f_string']
            deleter_execute_on_persist = True
        
        class ItemGeneralTwo(Item):
            model_cls = self.ModelGeneralTwo
            creators = [{'f_integer', 'f_string'}]
            getters = [{'f_integer', 'f_string'}]
            deleter_selectors = ['f_string']
        
        persister = self.persister
        get_key = lambda model: (model.f_string, model.f_integer)
        
        # creating items
        item_one_bulk = ItemGeneralOne.Bulk()
        item_two_bulk = ItemGeneralTwo.Bulk()
        for i in range(1, 3):
            item_one_bulk.gen(f_integer=100+i, f_string='source-1')
            item_two_bulk.gen(f_integer=100+i, f_string='source-1')
        
        persister.persist(item_one_bulk)
        persister.persist(item_two_bulk)
        
        # recreating items (first item from bulk one must be deleted)
        item_one_bulk = ItemGeneralOne.Bulk()
        item_two_bulk = ItemGeneralTwo.Bulk()
        for i in range(2, 4):
            item_one_bulk.gen(f_integer=100+i, f_string='source-1')
            item_two_bulk.gen(f_integer=100+i, f_string='source-1')
        
        persister.persist(item_one_bulk)
        persister.persist(item_two_bulk)
        
        models_one = self.get_all_models(self.ModelGeneralOne,
                                         sort_key=get_key)
        model_one_keys = [get_key(model) for model in models_one]
        expect = [('source-1', 102), ('source-1', 103)]
        self.assertEqual(model_one_keys, expect)
        
        models_two = self.get_all_models(self.ModelGeneralTwo,
                                         sort_key=get_key)
        model_two_keys = [get_key(model) for model in models_two]
        expect = [('source-1', 101), ('source-1', 102), ('source-1', 103)]
        self.assertEqual(model_two_keys, expect)
        
    
    def test_null_getters_and_creators(self):
        class ItemGeneralOne(Item):
            model_cls = self.ModelGeneralOne
            creators = [{'f_integer', 'f_float', 'f_string', 'f_text'}]
            getters = [{'f_integer', 'f_string'}]
            nullables = ['f_string']
        
        class ItemGeneralTwo(Item):
            model_cls = self.ModelGeneralTwo
        
        persister = self.persister
        get_key = lambda model: (model.f_string if model.f_string else '-',
                                 model.f_float,
                                 model.f_integer,
                                 model.f_text)
        
        bulk_item = ItemGeneralOne.Bulk()
        for i in range(3):
            item = bulk_item.gen(
                f_integer=i+1,
                f_string='str-{}'.format(i+1) if i > 1 else None,
                f_text='text-{}'.format(i+1))
            if i != 0:
                item['f_float'] = i+1 + (i+1)/10
        persister.persist(bulk_item)
        
        model_ones = self.get_all_models(self.ModelGeneralOne,
                                         sort_key=get_key)
        model_one_keys = [get_key(model) for model in model_ones]
        expect = [
            # first item cannot be created (missing `f_float`)
            # '-' stands for `None` string (otherwise not sortable)
            ('-', 2.2, 2, 'text-2'),
            ('str-3', 3.3, 3, 'text-3'),
        ]
        self.assertEqual(model_one_keys, expect)
        
        bulk_item = ItemGeneralOne.Bulk()
        for i in range(3):
            item = bulk_item.gen(
                f_integer=i+1,
                f_string='str-{}'.format(i+1) if i > 1 else None,
                f_text='text-{}'.format(i+1 + 100))
            if i != 0:
                item['f_float'] = i+1 + (i+1)/10
        persister.persist(bulk_item)
        
        model_ones = self.get_all_models(self.ModelGeneralOne,
                                         sort_key=get_key)
        model_one_keys = [get_key(model) for model in model_ones]
        expect = [
            ('-', 2.2, 2, 'text-102'),
            ('str-3', 3.3, 3, 'text-103'),
        ]
        self.assertEqual(model_one_keys, expect)
        
        
    def test_model_unrefs(self):
        class ItemGeneralOne(Item):
            model_cls = self.ModelGeneralOne
            creators = [{'f_integer'}]
            getters = [{'f_integer'}]
            unref_x_to_many = {
                'two_1_x': ['f_string'],
                'two_x_x': ['f_string']
            }
        
        class ItemGeneralTwo(Item):
            model_cls = self.ModelGeneralTwo
            creators = [{'f_integer', 'f_string'}]
            getters = [{'f_integer', 'f_string'}]
        
        persister = self.persister
        get_key = lambda model: (model.f_text, model.f_string, model.f_integer)
        
        item_one = ItemGeneralOne(f_integer=100)
        for source_name in ['src-1', 'src-2']:
            for i in range(1, 3):
                item_one['two_1_x'].gen(f_integer=200+i, f_string=source_name,
                                        f_text='two_1_x')
                item_one['two_x_x'].gen(f_integer=900+i, f_string=source_name,
                                        f_text='two_x_x')
        persister.persist(item_one)
        
        model_ones = self.get_all_models(self.ModelGeneralOne)
        self.assertEqual(len(model_ones), 1)
        model_one = model_ones[0]
        self.assertEqual(model_one.f_integer, 100)
        two_1_x = self.get_related_x_to_many(model_one, 'two_1_x',
                                             sort_key=get_key)
        two_x_x = self.get_related_x_to_many(model_one, 'two_x_x',
                                             sort_key=get_key)
        self.assertEqual(len(two_1_x), 4)
        self.assertEqual(len(two_x_x), 4)
        keys = [get_key(model) for model in chain(two_1_x, two_x_x)]
        expect = [
            ('two_1_x', 'src-1', 201),
            ('two_1_x', 'src-1', 202),
            ('two_1_x', 'src-2', 201),
            ('two_1_x', 'src-2', 202),
            ('two_x_x', 'src-1', 901),
            ('two_x_x', 'src-1', 902),
            ('two_x_x', 'src-2', 901),
            ('two_x_x', 'src-2', 902)
        ]
        self.assertEqual(keys, expect)
        
        item_one = ItemGeneralOne(f_integer=100)
        for source_name in ['src-1', 'src-2']:
            for i in range(2, 4):
                item_one['two_1_x'].gen(f_integer=200+i, f_string=source_name,
                                        f_text='two_1_x')
                item_one['two_x_x'].gen(f_integer=900+i, f_string=source_name,
                                        f_text='two_x_x')
        persister.persist(item_one)
        model_ones = self.get_all_models(self.ModelGeneralOne)
        self.assertEqual(len(model_ones), 1)
        model_one = model_ones[0]
        self.assertEqual(model_one.f_integer, 100)
        two_1_x = self.get_related_x_to_many(model_one, 'two_1_x',
                                             sort_key=get_key)
        two_x_x = self.get_related_x_to_many(model_one, 'two_x_x',
                                             sort_key=get_key)
        self.assertEqual(len(two_1_x), 4)
        self.assertEqual(len(two_x_x), 4)
        keys = [get_key(model) for model in chain(two_1_x, two_x_x)]
        # f_integer 201 and 901 were removed
        expect = [
            ('two_1_x', 'src-1', 202),
            ('two_1_x', 'src-1', 203),
            ('two_1_x', 'src-2', 202),
            ('two_1_x', 'src-2', 203),
            ('two_x_x', 'src-1', 902),
            ('two_x_x', 'src-1', 903),
            ('two_x_x', 'src-2', 902),
            ('two_x_x', 'src-2', 903)
        ]
        self.assertEqual(keys, expect)
        
        # f_integer 201 and 901 are still in database
        model_twos = self.get_all_models(self.ModelGeneralTwo,
                                         sort_key=get_key)
        keys = [get_key(model) for model in model_twos]
        expect = [
            ('two_1_x', 'src-1', 201),
            ('two_1_x', 'src-1', 202),
            ('two_1_x', 'src-1', 203),
            ('two_1_x', 'src-2', 201),
            ('two_1_x', 'src-2', 202),
            ('two_1_x', 'src-2', 203),
            ('two_x_x', 'src-1', 901),
            ('two_x_x', 'src-1', 902),
            ('two_x_x', 'src-1', 903),
            ('two_x_x', 'src-2', 901),
            ('two_x_x', 'src-2', 902),
            ('two_x_x', 'src-2', 903)
        ]
        self.assertEqual(keys, expect)
        
        
    def test_get_only_mode(self):
        
        class ItemGeneralOne(Item):
            model_cls = self.ModelGeneralOne
            creators = [{'f_integer'}]
            getters = [{'f_integer'}, {'two_x_x'}]
            
            def __str__(self):
                return 'ItemGeneralOne, f_integer: {}'.format(self['f_integer'])
            
        class ItemGeneralTwo(Item):
            model_cls = self.ModelGeneralTwo
            creators = [{'f_integer'}]
            getters = [{'f_integer'}]
            
            def __str__(self):
                return 'ItemGeneralTwo, f_integer: {}'.format(self['f_integer'])
        
        persister = self.persister
        get_key = lambda model: (model.f_integer,
                                 model.f_string if model.f_string else '')
        
        #--- normal model creating ---------------------------------------------
        bulk_item_one = ItemGeneralOne.Bulk()
        
        for i in range(2):
            bulk_item_one.gen(f_integer=i,
                              two_x_x=[ItemGeneralTwo(f_integer=i)])
        
        self.assertFalse(ItemGeneralOne.get_only_mode)
        self.assertFalse(ItemGeneralTwo.get_only_mode)
        
        persister.persist(bulk_item_one)
        model_ones = self.get_all_models(self.ModelGeneralOne, sort_key=get_key)
        
        self.assertEqual(len(model_ones), 2)
        self.assertEqual(model_ones[0].f_integer, 0)
        self.assertEqual(model_ones[1].f_integer, 1)
        
        two_x_x_first = self.get_related_x_to_many(model_ones[0], 'two_x_x',
                                                   sort_key=get_key)
        self.assertEqual(len(two_x_x_first), 1)
        self.assertEqual(two_x_x_first[0].f_integer, 0)
        
        two_x_x_second = self.get_related_x_to_many(model_ones[1], 'two_x_x',
                                                    sort_key=get_key)
        self.assertEqual(len(two_x_x_second), 1)
        self.assertEqual(two_x_x_second[0].f_integer, 1)
        
        #--- some items in get_only_mode ---------------------------------------
        bulk_item_one = ItemGeneralOne.Bulk()
        
        # get only (cannot be created)
        # (related by "two_x_x" field item must be created)
        not_saved_item = bulk_item_one.gen(
            f_integer=10, f_string='str-{}'.format(10),
            two_x_x=[ItemGeneralTwo(f_integer=10)])
        not_saved_item.get_only_mode = True
        
        # normal
        item = bulk_item_one.gen(f_integer=20,
                                 f_string='str-{}'.format(20),
                                 two_x_x=[ItemGeneralTwo(f_integer=20)])
        
        
        # old items
        for i in range(2):
            item = bulk_item_one.gen(
                f_integer=i, f_string='str-{}'.format(i),
                two_x_x=[ItemGeneralTwo(f_integer=i,
                                        f_string='str-{}'.format(i))])
            
            # second item update only
            if i == 1:
                del item['f_integer']  # forcing to use 'two_x_x' getter
                item.get_only_mode = True
                item['two_x_x'][0].get_only_mode = True
        
        
        saved_items, _ = persister.persist(bulk_item_one)
        
        # f_integer values are 0, 1, 20 (with f_integer=1 deleted)    
        self.assertEqual(len(saved_items), 3)
        self.assertNotIn(not_saved_item, saved_items)
        
        # all items can be loaded except for `f_integer=10` one
        for item in bulk_item_one:
            if item is not_saved_item:
                continue
            self.assertIn(item, saved_items)
        
        # checking the data
        model_ones = self.get_all_models(self.ModelGeneralOne, sort_key=get_key)
        self.assertEqual(len(model_ones), 3)
        
        self.assertEqual(model_ones[0].f_integer, 0)
        self.assertEqual(model_ones[1].f_integer, 1)
        self.assertEqual(model_ones[2].f_integer, 20)
        
        self.assertEqual(model_ones[0].f_string, 'str-0')
        self.assertIsNone(model_ones[1].f_string)  # get_only_mode
        self.assertEqual(model_ones[2].f_string, 'str-20')
        
        # checking model_two without model_one
        model_twos = self.get_all_models(self.ModelGeneralTwo, sort_key=get_key)
        
        self.assertEqual(len(model_twos), 4)
        model_two = model_twos[-2]  # with `f_integer=10`
        self.assertEqual(model_two.f_integer, 10)
        
        one_x_x = self.get_related_x_to_many(model_two, 'one_x_x')
        self.assertEqual(len(one_x_x), 0)  # get_only_mode
        
        # checking all other model_two
        two_x_x = self.get_related_x_to_many(model_ones[0], 'two_x_x',
                                             sort_key=get_key)
        self.assertEqual(len(two_x_x), 1)
        self.assertEqual(two_x_x[0].f_integer, 0)
        self.assertEqual(two_x_x[0].f_string, 'str-0')
        
        two_x_x = self.get_related_x_to_many(model_ones[1], 'two_x_x',
                                             sort_key=get_key)
        self.assertEqual(len(two_x_x), 1)
        self.assertEqual(two_x_x[0].f_integer, 1)
        self.assertIsNone(two_x_x[0].f_string)  # get_only_mode
        
        two_x_x = self.get_related_x_to_many(model_ones[2], 'two_x_x',
                                             sort_key=get_key)
        self.assertEqual(len(two_x_x), 1)
        self.assertEqual(two_x_x[0].f_integer, 20)