package azmalent.terraincognita.common.init;

import azmalent.terraincognita.TIConfig;
import azmalent.terraincognita.TerraIncognita;
import azmalent.terraincognita.common.inventory.BasketContainer;
import net.minecraft.inventory.container.ContainerType;
import net.minecraftforge.common.extensions.IForgeContainerType;
import net.minecraftforge.fml.RegistryObject;
import net.minecraftforge.fml.network.IContainerFactory;
import net.minecraftforge.registries.DeferredRegister;
import net.minecraftforge.registries.ForgeRegistries;

public class ModContainers {
    public static final DeferredRegister<ContainerType<?>> CONTAINERS = DeferredRegister.create(ForgeRegistries.CONTAINERS, TerraIncognita.MODID);

    public static RegistryObject<ContainerType<BasketContainer>> BASKET;

    static {
        if (TIConfig.Tools.basket.get()) {
            BASKET = CONTAINERS.register("basket", () -> IForgeContainerType.create(BasketContainer::new));
        }
    }
}
