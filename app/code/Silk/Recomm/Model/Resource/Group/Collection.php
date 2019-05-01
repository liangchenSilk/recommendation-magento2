<?php

namespace Silk\Recomm\Model\Resource\Group;

use Magento\Framework\Model\ResourceModel\Db\Collection\AbstractCollection;

class Collection extends AbstractCollection
{
    /**
     * Define model & resource model
     */
    protected function _construct()
    {
        $this->_init(
            'Silk\Recomm\Model\Group',
            'Silk\Recomm\Model\Resource\Group'
        );
    }
}
