from products import origin_models


class treeOfCategories(origin_models.TreeOfCategories):
    def __init__(self, id: str, all_categories: str, root_cat: str, subcategories: str, main_category: str):
        self.id = id
        self.all_categories = all_categories
        self.root_cat = root_cat
        self.subcategories = subcategories
        self.main_category = main_category
    def __repr__(self):
        return '{'+f'id: {self.id}, all_categories: {self.all_categories}, root_cat: {self.root_cat}, subcategories: {self.subcategories}, main_category: {self.main_category}'+'}'
    def __str__(self):
        return f'id: {self.id}, all_categories: {self.all_categories}, root_cat: {self.root_cat}, subcategories: {self.subcategories}, main_category: {self.main_category}'
    def __eq__(self, other):
        return self.id == other.id and self.all_categories == other.all_categories and self.root_cat == other.root_cat and self.subcategories == other.subcategories and self.main_category == other.main_category
    def __hash__(self):
        return hash(self.id) #this method is used to compare objects in sets
    def __bool__(self):
        return bool(self.id)
    def __copy__(self):
        return treeOfCategories(self.id, self.all_categories, self.root_cat, self.subcategories, self.main_category)
    def __getitem__(self, item):
        if item in self.__dict__:
            return self.__dict__[item]
        else:
            raise KeyError(f'Item {item} not found')
    def __setitem__(self, item, value):
        self.__dict__[item] = value
    def __contains__(self, item):
        return item in self.__dict__
    def __iter__(self):
        yield self.id
        yield self.all_categories
        yield self.root_cat
        yield self.subcategories
        yield self.main_category
    def __len__(self):
        return len(self.__dict__)
    #the subcategories are a list of names of the subcategories casted to a string
    def get_subcategories(self):
        return eval(self.subcategories)
    #also all_categories is a list of names of the categories casted to a string
    def get_all_categories(self):
        return eval(self.all_categories)
    #add the method to do .keys() and .values() to the object
    def keys(self):
        return self.__dict__.keys()
    def values(self):
        return self.__dict__.values()
    def items(self):
        return self.__dict__.items()
    def __call__(self, *args, **kwargs): #this method is used to call the object as a function
        return self.__dict__
    



class typesSpecs(origin_models.TypesSpecs):
    def __init__(self, T_id: int, types_specs: str):
        self.T_id = T_id
        self.types_specs = types_specs
    def __repr__(self):
        return '{'+f'T_id: {self.T_id}, types_specs: {self.types_specs}'+'}'
    def __str__(self):
        return f'T_id: {self.T_id}, types_specs: {self.types_specs}'
    def __eq__(self, other):
        return self.T_id == other.T_id and self.types_specs == other.types_specs
    def __hash__(self):
        return hash(self.T_id)
    def __copy__(self):
        return typesSpecs(self.T_id, self.types_specs)
    def __getitem__(self, item):
        if item in self.__dict__:
            return self.__dict__[item]
        else:
            raise KeyError(f'Item {item} not found')
    def __setitem__(self, item, value):
        self.__dict__[item] = value
    def __contains__(self, item):
        return item in self.__dict__
    def __iter__(self):
        yield self.T_id
        yield self.types_specs
    def __len__(self):
        return len(self.__dict__)

class products(origin_models.Products):
    def __init__(self, item_id: str, name: str, itm_description: str, category: str, datasheet_link: str, itms_val_in_pkg: str, img: str, path: str):
        self.item_id = item_id
        self.name = name
        self.itm_description = itm_description
        self.category = category
        self.datasheet_link = datasheet_link
        self.itms_val_in_pkg = itms_val_in_pkg
        self.img = img
        self.path = path
    def __repr__(self):
        return '{'+f'item_id: {self.item_id}, name: {self.name}, itm_description: {self.itm_description}, category: {self.category}, datasheet_link: {self.datasheet_link}, itms_val_in_pkg: {self.itms_val_in_pkg}, img: {self.img}, path: {self.path}'+'}'
    def __str__(self):
        return f'item_id: {self.item_id}, name: {self.name}, itm_description: {self.itm_description}, category: {self.category}, datasheet_link: {self.datasheet_link}, itms_val_in_pkg: {self.itms_val_in_pkg}, img: {self.img}, path: {self.path}'
    def __eq__(self, other):
        return self.item_id == other.item_id
    def __hash__(self):
        return hash(self.item_id)
    def __bool__(self):
        return bool(self.item_id)
    def __copy__(self):
        return products(self.item_id, self.name, self.itm_description, self.category, self.datasheet_link, self.itms_val_in_pkg, self.img, self.path)
    def __getitem__(self, item):
        if item in self.__dict__:
            return self.__dict__[item]
        else:
            raise KeyError(f'Item {item} not found')
    def __setitem__(self, item, value):
        self.__dict__[item] = value
    def __contains__(self, item):
        return item in self.__dict__
    def __iter__(self):
        yield self.item_id
        yield self.name
        yield self.itm_description
        yield self.category
        yield self.datasheet_link
        yield self.itms_val_in_pkg
        yield self.img
        yield self.path
    def __len__(self):
        return len(self.__dict__)
    def get_path(self):
        return eval(self.path)
    def keys(self):
        #drop ['_sa_instance_state'] from the keys
        return [key for key in self.__dict__.keys() if key != '_sa_instance_state']
    def values(self):
        return [value for value in self.__dict__.values() if value != '_sa_instance_state']
    def items(self):
        return [(key, value) for key, value in self.__dict__.items() if key != '_sa_instance_state']
    def __call__(self, *args, **kwargs):
        return self.__dict__

class specs(origin_models.Specs):
    def __init__(self, id: int, item_id: str, name: str, value: str, type: str):
        self.id = id
        self.item_id = item_id
        self.name = name
        self.value = value
        self.type = type
    def __repr__(self):
        return '{'+f'"id": "{self.id}", "item_id": "{self.item_id}", "{self.name}": "{self.value}", "type": "{self.type}"'+'}'
    def __str__(self):
        return f'id: {self.id}, item_id: {self.item_id}, name: {self.name}, value: {self.value}, type: {self.type}'
    def __eq__(self, other):
        return self.id == other.id
    def __hash__(self):
        return hash(self.id)
    def __bool__(self):
        return bool(self.id)
    def __copy__(self):
        return specs(self.id, self.item_id, self.name, self.value, self.type)
    def __getitem__(self, item):
        if item in self.__dict__:
            return self.__dict__[item]
        else:
            raise KeyError(f'Item {item} not found')
    def __setitem__(self, item, value):
        self.__dict__[item] = value
    def __contains__(self, item):
        return item in self.__dict__
    def __iter__(self):
        yield self.id
        yield self.item_id
        yield self.name
        yield self.value
        yield self.type
    def __len__(self):
        return len(self.__dict__)